import json
import asyncio
import logging
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from .base_agent import BaseAgent
import subprocess

class TerraformAgent(BaseAgent):
    """Agent for managing Terraform operations."""
    
    def __init__(self, work_dir: str = "./terraform_workspace"):
        super().__init__(work_dir)
        # Try to find Terraform in common locations on Windows
        self.terraform_bin = self._find_terraform()
        if not self.terraform_bin:
            raise RuntimeError(
                "Terraform not found. Please install Terraform and ensure it's in your PATH. "
                "Download from: https://www.terraform.io/downloads.html"
            )
        self.var_file = self.work_dir / "terraform.tfvars.json"
        self.state_file = self.work_dir / "terraform.tfstate"
        
    def _find_terraform(self) -> str:
        """Find Terraform executable with explicit path for Windows."""
        import os
        import logging
        from pathlib import Path
        
        logger = logging.getLogger(__name__)
        
        # Try explicit path first
        explicit_paths = [
            r'C:\\terraform\\terraform.exe',
            r'C:\\Program Files\\Terraform\\terraform.exe',
            r'C:\\Program Files (x86)\\Terraform\\terraform.exe'
        ]
        
        for path in explicit_paths:
            if os.path.isfile(path):
                logger.debug(f"Found Terraform at explicit path: {path}")
                return path  # Return raw path, let subprocess handle escaping
        
        # Fallback to PATH lookup
        logger.debug("Terraform not found in explicit paths, checking PATH...")
        if os.name == 'nt':  # Windows
            for cmd in ['terraform.exe', 'terraform']:
                path = shutil.which(cmd)
                if path and os.path.isfile(path):
                    abs_path = os.path.abspath(path)
                    logger.debug(f"Found Terraform in PATH: {abs_path}")
                    return abs_path  # Return raw path
        
        # If not found, log all searched paths and raise error
        searched_paths = '\n'.join([f"- {p}" for p in explicit_paths])
        error_msg = (
            "Terraform not found in any of the following locations:\n"
            f"{searched_paths}\n"
            "And not found in system PATH.\n"
            "Please install Terraform from: https://www.terraform.io/downloads.html\n"
            "And ensure it's either in one of the above locations or in your system PATH."
        )
        logger.error(error_msg)
        raise RuntimeError("Terraform executable not found. See logs for details.")
    
    def _run_command(self, *args: str) -> Dict[str, Any]:
        """Run a terraform command and return the result."""
        import logging
        import subprocess
        from pathlib import Path
        
        logger = logging.getLogger(__name__)
        
        # Prepare command and log it
        cmd_args = [self.terraform_bin] + list(args)
        cmd_str = ' '.join(f'"{arg}"' if ' ' in str(arg) else str(arg) for arg in cmd_args)
        logger.debug(f"Executing command: {cmd_str} in {self.work_dir}")
        
        try:
            # Ensure work_dir exists
            Path(self.work_dir).mkdir(parents=True, exist_ok=True)
            
            # Run the command using subprocess.run
            result = subprocess.run(
                cmd_args,
                cwd=str(self.work_dir),
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            # Log results
            if result.returncode != 0:
                logger.error(f"Command failed with code {result.returncode}")
                if result.stderr:
                    logger.error(f"Stderr: {result.stderr.strip()}")
            
            # Prepare result
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()
            }
            
        except Exception as e:
            error_msg = f"Error executing command: {str(e)}"
            logger.exception(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "returncode": -1,
                "stdout": "",
                "stderr": error_msg
            }
    
    def initialize(self):
        """Initialize the Terraform working directory."""
        logger = logging.getLogger(__name__)
        logger.info(f"Initializing Terraform in {self.work_dir}")
        
        # Ensure workspace directory exists
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a basic Terraform configuration if none exists
        main_tf = self.work_dir / "main.tf"
        if not main_tf.exists():
            logger.info("Creating default Terraform configuration")
            with open(main_tf, 'w', encoding='utf-8') as f:
                f.write("""
terraform {
  required_providers {
    null = {
      source = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

resource "null_resource" "example" {
  provisioner "local-exec" {
    command = "echo 'Terraform initialized successfully'"
  }
}
""")
        
        # Initialize Terraform
        logger.info("Running terraform init...")
        result = self._run_command("init", "-input=false")
        
        # Log detailed results
        if result.get("stdout"):
            logger.debug(f"Terraform init stdout: {result['stdout']}")
        if result.get("stderr"):
            logger.warning(f"Terraform init stderr: {result['stderr']}")
        
        # Check for success
        if not result.get("success", False):
            error_msg = result.get("stderr", result.get("error", "Unknown error during Terraform init"))
            if "No such file or directory" in error_msg:
                error_msg = f"Terraform executable not found at {self.terraform_bin}. Please verify installation."
            logger.error(f"Failed to initialize Terraform: {error_msg}")
            raise Exception(f"Failed to initialize Terraform: {error_msg}")
            
        logger.info("Terraform initialized successfully")
        return result
    
    async def plan(self, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a Terraform plan."""
        if config:
            with open(self.var_file, 'w') as f:
                json.dump(config, f)
        
        plan_file = self.work_dir / "tfplan"
        result = await self._run_command("plan", "-out=tfplan", "-input=false")
        
        if result["success"]:
            self.state["plan_file"] = str(plan_file)
        
        return result
    
    async def apply(self, plan: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Apply the Terraform configuration."""
        if plan and "plan_file" in plan:
            result = await self._run_command("apply", "-auto-approve", plan["plan_file"])
        else:
            result = await self._run_command("apply", "-auto-approve")
        
        if result["success"]:
            output = await self._run_command("output", "-json")
            if output["success"]:
                self.state["outputs"] = json.loads(output["stdout"])
        
        return result
    
    async def destroy(self) -> Dict[str, Any]:
        """Destroy all managed resources."""
        return await self._run_command("destroy", "-auto-approve")
    
    async def show(self) -> Dict[str, Any]:
        """Show the current state."""
        return await self._run_command("show", "-json")
    
    async def validate(self) -> Dict[str, Any]:
        """Validate the Terraform configuration."""
        return await self._run_command("validate")
