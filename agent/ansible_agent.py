import asyncio
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
import subprocess

class AnsibleAgent(BaseAgent):
    """Agent for managing Ansible operations."""
    
    def __init__(self, work_dir: str = "./ansible_workspace"):
        super().__init__(work_dir)
        self.ansible_playbook_bin = "ansible-playbook"
        self.inventory_file = self.work_dir / "inventory.ini"
        self.playbook_file = self.work_dir / "playbook.yml"
    
    async def _run_command(self, *args: str) -> Dict[str, Any]:
        """Run an Ansible command and return the result."""
        try:
            process = await asyncio.create_subprocess_exec(
                self.ansible_playbook_bin,
                *args,
                cwd=str(self.work_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "returncode": process.returncode,
                "stdout": stdout.decode().strip(),
                "stderr": stderr.decode().strip()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_inventory(self, inventory: Dict[str, Any]) -> None:
        """Create an Ansible inventory file."""
        inventory_content = []
        
        for group, hosts in inventory.items():
            if isinstance(hosts, list):
                inventory_content.append(f"[{group}]") 
                for host in hosts:
                    inventory_content.append(host)
                inventory_content.append("")
        
        with open(self.inventory_file, 'w') as f:
            f.write("\n".join(inventory_content))
    
    async def create_playbook(self, playbook: Dict[str, Any]) -> None:
        """Create an Ansible playbook file."""
        with open(self.playbook_file, 'w') as f:
            yaml.dump(playbook, f, default_flow_style=False)
    
    async def run_playbook(
        self, 
        playbook: Optional[Dict[str, Any]] = None,
        inventory: Optional[Dict[str, Any]] = None,
        extra_vars: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Run an Ansible playbook."""
        if playbook:
            await self.create_playbook(playbook)
        
        if inventory:
            await self.create_inventory(inventory)
        
        cmd = [str(self.playbook_file)]
        
        if extra_vars:
            extra_vars_file = self.work_dir / "extra_vars.json"
            with open(extra_vars_file, 'w') as f:
                json.dump(extra_vars, f)
            cmd.extend(["-e", f"@{extra_vars_file}"])
        
        if self.inventory_file.exists():
            cmd.extend(["-i", str(self.inventory_file)])
        
        return await self._run_command(*cmd)
    
    async def ping(self, host_pattern: str = "all") -> Dict[str, Any]:
        """Test connectivity to hosts."""
        cmd = [
            "ansible",
            host_pattern,
            "-m", "ping"
        ]
        
        if self.inventory_file.exists():
            cmd.extend(["-i", str(self.inventory_file)])
        
        return await self._run_command(*cmd)
    
    async def get_facts(self, host_pattern: str = "all") -> Dict[str, Any]:
        """Gather facts about hosts."""
        cmd = [
            "ansible",
            host_pattern,
            "-m", "setup"
        ]
        
        if self.inventory_file.exists():
            cmd.extend(["-i", str(self.inventory_file)])
        
        return await self._run_command(*cmd)
