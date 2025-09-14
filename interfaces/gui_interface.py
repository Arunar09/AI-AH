#!/usr/bin/env python3
"""
GUI Interface for Intelligent Agents
Provides visual interface with drag-and-drop requirement gathering and real-time planning
"""

import sys
import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import threading
import webbrowser

# Add parent directory to path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
intelligent_agents_dir = parent_dir / "intelligent-agents"
sys.path.insert(0, str(intelligent_agents_dir))

try:
    from agents.terraform.intelligent_terraform_agent import IntelligentTerraformAgent
    from core.reasoning.local_reasoning_engine import LocalReasoningEngine
except ImportError as e:
    print(f"Warning: Could not import agents: {e}")
    print("Running in demo mode without agent integration")
    IntelligentTerraformAgent = None
    LocalReasoningEngine = None

class RequirementWidget:
    """Individual requirement widget with validation"""
    
    def __init__(self, parent, requirement_data, on_change_callback=None):
        self.parent = parent
        self.requirement_data = requirement_data
        self.on_change_callback = on_change_callback
        self.frame = None
        self.entry = None
        self.validation_label = None
        self.create_widget()
    
    def create_widget(self):
        """Create the requirement widget"""
        self.frame = ttk.Frame(self.parent)
        
        # Question label
        question_label = ttk.Label(
            self.frame, 
            text=self.requirement_data["question"],
            font=("Arial", 10, "bold"),
            wraplength=600
        )
        question_label.pack(anchor="w", pady=(0, 5))
        
        # Validation rules info
        if self.requirement_data.get("validation_rules"):
            rules_text = " | ".join(self.requirement_data["validation_rules"])
            rules_label = ttk.Label(
                self.frame,
                text=f"Rules: {rules_text}",
                font=("Arial", 8),
                foreground="gray"
            )
            rules_label.pack(anchor="w", pady=(0, 5))
        
        # Input field
        if self.requirement_data.get("type") == "multiline":
            self.entry = scrolledtext.ScrolledText(
                self.frame,
                height=3,
                width=70,
                wrap=tk.WORD
            )
        else:
            self.entry = ttk.Entry(self.frame, width=70)
        
        self.entry.pack(anchor="w", pady=(0, 5))
        self.entry.bind("<KeyRelease>", self.on_input_change)
        
        # Validation status
        self.validation_label = ttk.Label(
            self.frame,
            text="",
            font=("Arial", 8)
        )
        self.validation_label.pack(anchor="w")
        
        # Follow-up questions
        if self.requirement_data.get("follow_up_questions"):
            follow_up_frame = ttk.Frame(self.frame)
            follow_up_frame.pack(anchor="w", pady=(10, 0))
            
            ttk.Label(
                follow_up_frame,
                text="Follow-up Questions:",
                font=("Arial", 9, "bold")
            ).pack(anchor="w")
            
            for follow_up in self.requirement_data["follow_up_questions"]:
                follow_up_label = ttk.Label(
                    follow_up_frame,
                    text=f"• {follow_up}",
                    font=("Arial", 8),
                    foreground="blue"
                )
                follow_up_label.pack(anchor="w", padx=(20, 0))
    
    def on_input_change(self, event=None):
        """Handle input change"""
        value = self.entry.get("1.0", tk.END).strip() if hasattr(self.entry, "get") else self.entry.get()
        
        # Validate input
        is_valid = self.validate_input(value)
        
        # Update validation status
        if is_valid:
            self.validation_label.config(text="✅ Valid", foreground="green")
        else:
            self.validation_label.config(text="❌ Invalid", foreground="red")
        
        # Call callback
        if self.on_change_callback:
            self.on_change_callback(self.requirement_data["category"], value, is_valid)
    
    def validate_input(self, value: str) -> bool:
        """Validate input against rules"""
        rules = self.requirement_data.get("validation_rules", [])
        
        if not value and "not_empty" in rules:
            return False
        
        for rule in rules:
            if rule.startswith("one_of:"):
                options = rule.split(":")[1].split(",")
                if value.lower() not in [opt.lower() for opt in options]:
                    return False
            elif rule.startswith("numeric_range:"):
                try:
                    num_value = float(value)
                    range_str = rule.split(":")[1]
                    min_val, max_val = map(float, range_str.split("-"))
                    if not (min_val <= num_value <= max_val):
                        return False
                except ValueError:
                    return False
        
        return True
    
    def get_value(self) -> str:
        """Get current value"""
        if hasattr(self.entry, "get"):
            return self.entry.get("1.0", tk.END).strip()
        return self.entry.get()
    
    def set_value(self, value: str):
        """Set value"""
        if hasattr(self.entry, "insert"):
            self.entry.delete("1.0", tk.END)
            self.entry.insert("1.0", value)
        else:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, value)

class ProjectWizard:
    """Project creation wizard with step-by-step requirement collection"""
    
    def __init__(self, parent, on_complete_callback=None):
        self.parent = parent
        self.on_complete_callback = on_complete_callback
        self.current_step = 0
        self.requirements = {}
        self.requirement_widgets = {}
        self.validation_status = {}
        
        # Project type templates
        self.project_templates = {
            "Web Application": {
                "description": "Traditional web application with frontend and backend",
                "requirements": [
                    {
                        "category": "basic_info",
                        "question": "What is the name of your project?",
                        "type": "text",
                        "validation_rules": ["not_empty", "alphanumeric"],
                        "follow_up_questions": [
                            "What is the primary purpose of this application?",
                            "Who are the target users?"
                        ]
                    },
                    {
                        "category": "infrastructure",
                        "question": "Which cloud provider do you prefer?",
                        "type": "dropdown",
                        "options": ["AWS", "Azure", "GCP", "Multi-cloud"],
                        "validation_rules": ["one_of:aws,azure,gcp,multi-cloud"]
                    },
                    {
                        "category": "scaling",
                        "question": "What is your expected user load?",
                        "type": "number",
                        "validation_rules": ["numeric_range:1-10000000"],
                        "follow_up_questions": [
                            "What is your peak traffic pattern?",
                            "Do you need auto-scaling?"
                        ]
                    },
                    {
                        "category": "budget",
                        "question": "What is your monthly budget?",
                        "type": "number",
                        "validation_rules": ["numeric_range:10-50000"]
                    },
                    {
                        "category": "security",
                        "question": "What are your security requirements?",
                        "type": "multiline",
                        "validation_rules": ["not_empty"]
                    }
                ]
            },
            "Microservices": {
                "description": "Containerized microservices architecture",
                "requirements": [
                    {
                        "category": "architecture",
                        "question": "How many microservices do you plan to deploy?",
                        "type": "number",
                        "validation_rules": ["numeric_range:1-100"]
                    },
                    {
                        "category": "containerization",
                        "question": "Which container orchestration platform?",
                        "type": "dropdown",
                        "options": ["EKS", "AKS", "GKE", "ECS"],
                        "validation_rules": ["one_of:eks,aks,gke,ecs"]
                    },
                    {
                        "category": "communication",
                        "question": "What is the communication pattern between services?",
                        "type": "dropdown",
                        "options": ["REST API", "GraphQL", "gRPC", "Message Queue"],
                        "validation_rules": ["not_empty"]
                    }
                ]
            },
            "Data Platform": {
                "description": "Data processing and analytics platform",
                "requirements": [
                    {
                        "category": "data_volume",
                        "question": "What is your expected data volume?",
                        "type": "number",
                        "validation_rules": ["numeric_range:1-1000000"]
                    },
                    {
                        "category": "analytics",
                        "question": "What type of analytics do you need?",
                        "type": "dropdown",
                        "options": ["Batch", "Streaming", "Interactive", "ML"],
                        "validation_rules": ["one_of:batch,streaming,interactive,ml"]
                    },
                    {
                        "category": "processing",
                        "question": "What is your data processing latency requirement?",
                        "type": "dropdown",
                        "options": ["Real-time (<1s)", "Near real-time (<1min)", "Batch (<1hour)", "Flexible"],
                        "validation_rules": ["not_empty"]
                    }
                ]
            }
        }
        
        self.create_wizard()
    
    def create_wizard(self):
        """Create the wizard interface"""
        self.wizard_window = tk.Toplevel(self.parent)
        self.wizard_window.title("Project Creation Wizard")
        self.wizard_window.geometry("800x600")
        self.wizard_window.resizable(True, True)
        
        # Main frame
        main_frame = ttk.Frame(self.wizard_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = ttk.Label(
            header_frame,
            text="Project Creation Wizard",
            font=("Arial", 16, "bold")
        )
        self.title_label.pack()
        
        self.step_label = ttk.Label(
            header_frame,
            text="Step 1: Select Project Type",
            font=("Arial", 12)
        )
        self.step_label.pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(
            header_frame,
            mode='determinate',
            length=400
        )
        self.progress.pack(pady=(10, 0))
        
        # Content frame
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Navigation frame
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.back_button = ttk.Button(
            nav_frame,
            text="← Back",
            command=self.previous_step,
            state=tk.DISABLED
        )
        self.back_button.pack(side=tk.LEFT)
        
        self.next_button = ttk.Button(
            nav_frame,
            text="Next →",
            command=self.next_step
        )
        self.next_button.pack(side=tk.RIGHT)
        
        # Start with project type selection
        self.show_project_type_selection()
    
    def show_project_type_selection(self):
        """Show project type selection step"""
        self.current_step = 0
        self.step_label.config(text="Step 1: Select Project Type")
        self.progress.config(value=0)
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Project type selection
        ttk.Label(
            self.content_frame,
            text="Choose the type of project you want to create:",
            font=("Arial", 12)
        ).pack(pady=(0, 20))
        
        self.selected_project_type = tk.StringVar()
        
        for project_type, details in self.project_templates.items():
            frame = ttk.Frame(self.content_frame)
            frame.pack(fill=tk.X, pady=5)
            
            radio = ttk.Radiobutton(
                frame,
                text=project_type,
                variable=self.selected_project_type,
                value=project_type,
                command=self.on_project_type_selected
            )
            radio.pack(side=tk.LEFT)
            
            desc_label = ttk.Label(
                frame,
                text=details["description"],
                font=("Arial", 9),
                foreground="gray"
            )
            desc_label.pack(side=tk.LEFT, padx=(10, 0))
        
        self.next_button.config(text="Next →", state=tk.DISABLED)
    
    def on_project_type_selected(self):
        """Handle project type selection"""
        self.next_button.config(state=tk.NORMAL)
    
    def show_requirements_collection(self):
        """Show requirements collection step"""
        self.current_step = 1
        project_type = self.selected_project_type.get()
        requirements = self.project_templates[project_type]["requirements"]
        
        self.step_label.config(text=f"Step 2: Requirements for {project_type}")
        self.progress.config(value=50)
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        canvas = tk.Canvas(self.content_frame)
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create requirement widgets
        self.requirement_widgets = {}
        for req_data in requirements:
            widget = RequirementWidget(
                scrollable_frame,
                req_data,
                self.on_requirement_change
            )
            widget.frame.pack(fill=tk.X, pady=10, padx=10)
            self.requirement_widgets[req_data["category"]] = widget
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Update navigation
        self.next_button.config(text="Generate Plan →", state=tk.DISABLED)
        self.back_button.config(state=tk.NORMAL)
    
    def on_requirement_change(self, category: str, value: str, is_valid: bool):
        """Handle requirement change"""
        self.requirements[category] = value
        self.validation_status[category] = is_valid
        
        # Check if all required fields are valid
        all_valid = all(self.validation_status.values())
        self.next_button.config(state=tk.NORMAL if all_valid else tk.DISABLED)
    
    def show_plan_generation(self):
        """Show plan generation step"""
        self.current_step = 2
        self.step_label.config(text="Step 3: Generating Your Plan")
        self.progress.config(value=100)
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Show loading
        loading_label = ttk.Label(
            self.content_frame,
            text="🤖 Generating your infrastructure plan...",
            font=("Arial", 14)
        )
        loading_label.pack(pady=50)
        
        # Progress bar for generation
        gen_progress = ttk.Progressbar(
            self.content_frame,
            mode='indeterminate',
            length=400
        )
        gen_progress.pack(pady=20)
        gen_progress.start()
        
        # Generate plan in background
        self.generate_plan_async()
        
        # Update navigation
        self.next_button.config(text="Complete", command=self.complete_wizard)
        self.back_button.config(state=tk.NORMAL)
    
    def generate_plan_async(self):
        """Generate plan asynchronously"""
        def generate():
            try:
                # Create agent
                agent = IntelligentTerraformAgent()
                
                # Generate request from requirements
                request = self.generate_request_from_requirements()
                
                # Process with agent
                response = agent.process_request(request)
                
                # Store results
                self.generated_plan = {
                    "project_type": self.selected_project_type.get(),
                    "requirements": self.requirements,
                    "request": request,
                    "response": asdict(response)
                }
                
                # Update UI in main thread
                self.wizard_window.after(0, self.show_generated_plan)
                
            except Exception as e:
                self.wizard_window.after(0, lambda: self.show_error(str(e)))
        
        # Start generation in background thread
        thread = threading.Thread(target=generate)
        thread.daemon = True
        thread.start()
    
    def generate_request_from_requirements(self) -> str:
        """Generate request string from requirements"""
        request_parts = []
        
        for category, value in self.requirements.items():
            if value:
                # Find the question for this category
                project_type = self.selected_project_type.get()
                requirements = self.project_templates[project_type]["requirements"]
                
                for req in requirements:
                    if req["category"] == category:
                        request_parts.append(f"{req['question']}: {value}")
                        break
        
        return "\n".join(request_parts)
    
    def show_generated_plan(self):
        """Show the generated plan"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Plan summary
        ttk.Label(
            self.content_frame,
            text="✅ Your Infrastructure Plan is Ready!",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))
        
        # Plan details
        plan_frame = ttk.Frame(self.content_frame)
        plan_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cost and confidence
        response = self.generated_plan["response"]
        cost_frame = ttk.Frame(plan_frame)
        cost_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(cost_frame, text=f"💰 Estimated Cost: ${response['cost_estimate']}/month", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        ttk.Label(cost_frame, text=f"🎯 Confidence: {response['confidence'] * 100:.1f}%", font=("Arial", 12, "bold")).pack(side=tk.RIGHT)
        
        # Implementation steps
        steps_frame = ttk.LabelFrame(plan_frame, text="Implementation Steps", padding=10)
        steps_frame.pack(fill=tk.X, pady=10)
        
        for i, step in enumerate(response['implementation_steps'], 1):
            ttk.Label(steps_frame, text=f"{i}. {step}").pack(anchor="w")
        
        # Generated files
        files_frame = ttk.LabelFrame(plan_frame, text="Generated Files", padding=10)
        files_frame.pack(fill=tk.X, pady=10)
        
        for filename in response['terraform_code'].keys():
            ttk.Label(files_frame, text=f"✅ {filename}").pack(anchor="w")
        
        # Detailed explanation
        explanation_frame = ttk.LabelFrame(plan_frame, text="Detailed Explanation", padding=10)
        explanation_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        explanation_text = scrolledtext.ScrolledText(
            explanation_frame,
            height=8,
            wrap=tk.WORD
        )
        explanation_text.pack(fill=tk.BOTH, expand=True)
        explanation_text.insert("1.0", response['content'])
        explanation_text.config(state=tk.DISABLED)
    
    def show_error(self, error_message: str):
        """Show error message"""
        messagebox.showerror("Error", f"Failed to generate plan: {error_message}")
    
    def previous_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            if self.current_step == 1:
                self.show_project_type_selection()
            elif self.current_step == 2:
                self.show_requirements_collection()
    
    def next_step(self):
        """Go to next step"""
        if self.current_step == 0:
            self.show_requirements_collection()
        elif self.current_step == 1:
            self.show_plan_generation()
    
    def complete_wizard(self):
        """Complete the wizard"""
        if hasattr(self, 'generated_plan'):
            if self.on_complete_callback:
                self.on_complete_callback(self.generated_plan)
            self.wizard_window.destroy()
        else:
            messagebox.showwarning("Warning", "Plan generation is still in progress. Please wait.")

class ScalingPlanViewer:
    """Viewer for production scaling plans"""
    
    def __init__(self, parent, scaling_plan):
        self.parent = parent
        self.scaling_plan = scaling_plan
        self.create_viewer()
    
    def create_viewer(self):
        """Create the scaling plan viewer"""
        self.viewer_window = tk.Toplevel(self.parent)
        self.viewer_window.title("Production Scaling Plan")
        self.viewer_window.geometry("900x700")
        self.viewer_window.resizable(True, True)
        
        # Main frame
        main_frame = ttk.Frame(self.viewer_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="📈 Production Scaling Plan",
            font=("Arial", 16, "bold")
        ).pack()
        
        # Plan overview
        overview_frame = ttk.LabelFrame(main_frame, text="Plan Overview", padding=10)
        overview_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(overview_frame, text=f"⏱️ Estimated Duration: {self.scaling_plan['estimated_duration']}").pack(anchor="w")
        ttk.Label(overview_frame, text=f"🎯 Current State: {self.scaling_plan['current_state']}").pack(anchor="w")
        ttk.Label(overview_frame, text=f"🚀 Target State: {self.scaling_plan['target_state']}").pack(anchor="w")
        
        # Phases
        phases_frame = ttk.LabelFrame(main_frame, text="Deployment Phases", padding=10)
        phases_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create notebook for phases
        notebook = ttk.Notebook(phases_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        for i, phase in enumerate(self.scaling_plan['phases']):
            phase_frame = ttk.Frame(notebook)
            notebook.add(phase_frame, text=f"Phase {i+1}: {phase['name']}")
            
            # Phase details
            ttk.Label(phase_frame, text=f"Duration: {phase['duration']}", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 10))
            
            # Steps
            ttk.Label(phase_frame, text="Steps:", font=("Arial", 10, "bold")).pack(anchor="w")
            
            for j, step in enumerate(phase['steps'], 1):
                step_frame = ttk.Frame(phase_frame)
                step_frame.pack(fill=tk.X, pady=2)
                
                ttk.Label(step_frame, text=f"{j}.", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
                ttk.Label(step_frame, text=step, font=("Arial", 9)).pack(side=tk.LEFT, padx=(5, 0))
        
        # Cost and risks
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X)
        
        # Cost implications
        cost_frame = ttk.LabelFrame(bottom_frame, text="Cost Implications", padding=10)
        cost_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        for cost_type, cost_range in self.scaling_plan['cost_implications'].items():
            ttk.Label(cost_frame, text=f"{cost_type.replace('_', ' ').title()}: {cost_range}").pack(anchor="w")
        
        # Risk assessment
        risk_frame = ttk.LabelFrame(bottom_frame, text="Risk Assessment", padding=10)
        risk_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        for risk in self.scaling_plan['risk_assessment']:
            ttk.Label(risk_frame, text=f"⚠️ {risk}").pack(anchor="w")

class TroubleshootingInterface:
    """Troubleshooting interface with interactive problem solving"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_interface()
    
    def create_interface(self):
        """Create troubleshooting interface"""
        self.troubleshoot_window = tk.Toplevel(self.parent)
        self.troubleshoot_window.title("Troubleshooting Assistant")
        self.troubleshoot_window.geometry("800x600")
        self.troubleshoot_window.resizable(True, True)
        
        # Main frame
        main_frame = ttk.Frame(self.troubleshoot_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        ttk.Label(
            main_frame,
            text="🔧 Infrastructure Troubleshooting Assistant",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))
        
        # Problem categories
        categories_frame = ttk.LabelFrame(main_frame, text="Problem Categories", padding=10)
        categories_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Category buttons
        categories = [
            ("🏗️ Infrastructure", self.show_infrastructure_troubleshooting),
            ("🚀 Deployment", self.show_deployment_troubleshooting),
            ("⚡ Performance", self.show_performance_troubleshooting),
            ("🔒 Security", self.show_security_troubleshooting),
            ("💰 Cost", self.show_cost_troubleshooting)
        ]
        
        for i, (category, command) in enumerate(categories):
            btn = ttk.Button(
                categories_frame,
                text=category,
                command=command
            )
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")
        
        categories_frame.columnconfigure(0, weight=1)
        categories_frame.columnconfigure(1, weight=1)
        
        # Content area
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Show initial help
        self.show_initial_help()
    
    def show_initial_help(self):
        """Show initial help"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        help_text = """
Welcome to the Infrastructure Troubleshooting Assistant!

This tool helps you diagnose and resolve common infrastructure issues:

🏗️ Infrastructure Issues
- Terraform state problems
- Resource conflicts
- Configuration errors
- Network issues

🚀 Deployment Issues
- Build failures
- Deployment timeouts
- Service startup problems
- Environment differences

⚡ Performance Issues
- Slow response times
- High resource usage
- Scaling problems
- Bottleneck identification

🔒 Security Issues
- Access control problems
- Certificate issues
- Compliance violations
- Vulnerability assessment

💰 Cost Issues
- Unexpected charges
- Resource optimization
- Budget overruns
- Cost analysis

Click on any category above to start troubleshooting!
        """
        
        ttk.Label(
            self.content_frame,
            text=help_text,
            font=("Arial", 10),
            justify=tk.LEFT
        ).pack(pady=20)
    
    def show_infrastructure_troubleshooting(self):
        """Show infrastructure troubleshooting"""
        self.show_troubleshooting_category("Infrastructure", [
            "Terraform state is locked",
            "Resource already exists error",
            "Permission denied errors",
            "Circular dependency error",
            "VPC configuration issues",
            "Security group problems",
            "Load balancer configuration",
            "Database connection issues"
        ])
    
    def show_deployment_troubleshooting(self):
        """Show deployment troubleshooting"""
        self.show_troubleshooting_category("Deployment", [
            "Build pipeline failures",
            "Deployment timeouts",
            "Service startup issues",
            "Environment configuration",
            "Container registry problems",
            "CI/CD pipeline issues",
            "Rollback procedures",
            "Health check failures"
        ])
    
    def show_performance_troubleshooting(self):
        """Show performance troubleshooting"""
        self.show_troubleshooting_category("Performance", [
            "Slow response times",
            "High CPU usage",
            "Memory leaks",
            "Database performance",
            "Network latency",
            "Auto-scaling issues",
            "Resource bottlenecks",
            "Cache problems"
        ])
    
    def show_security_troubleshooting(self):
        """Show security troubleshooting"""
        self.show_troubleshooting_category("Security", [
            "Access control issues",
            "Certificate problems",
            "Compliance violations",
            "Vulnerability scanning",
            "IAM policy errors",
            "Network security",
            "Data encryption",
            "Audit logging"
        ])
    
    def show_cost_troubleshooting(self):
        """Show cost troubleshooting"""
        self.show_troubleshooting_category("Cost", [
            "Unexpected charges",
            "Resource optimization",
            "Budget overruns",
            "Cost analysis",
            "Reserved instances",
            "Spot instance usage",
            "Storage optimization",
            "Network cost reduction"
        ])
    
    def show_troubleshooting_category(self, category: str, issues: List[str]):
        """Show troubleshooting category with issues"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Category header
        ttk.Label(
            self.content_frame,
            text=f"🔧 {category} Troubleshooting",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 20))
        
        # Issues list
        ttk.Label(
            self.content_frame,
            text="Select an issue to get detailed troubleshooting steps:",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(0, 10))
        
        # Issues frame
        issues_frame = ttk.Frame(self.content_frame)
        issues_frame.pack(fill=tk.X, pady=(0, 20))
        
        for i, issue in enumerate(issues):
            btn = ttk.Button(
                issues_frame,
                text=issue,
                command=lambda i=issue: self.show_issue_solution(i)
            )
            btn.pack(fill=tk.X, pady=2)
        
        # Back button
        ttk.Button(
            self.content_frame,
            text="← Back to Categories",
            command=self.show_initial_help
        ).pack(pady=10)
    
    def show_issue_solution(self, issue: str):
        """Show solution for specific issue"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Issue header
        ttk.Label(
            self.content_frame,
            text=f"🔍 {issue}",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 20))
        
        # Get solution (this would be expanded with real solutions)
        solution = self.get_issue_solution(issue)
        
        # Diagnosis
        diagnosis_frame = ttk.LabelFrame(self.content_frame, text="Diagnosis", padding=10)
        diagnosis_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(diagnosis_frame, text=solution["diagnosis"], font=("Arial", 10)).pack(anchor="w")
        
        # Solutions
        solutions_frame = ttk.LabelFrame(self.content_frame, text="Solutions", padding=10)
        solutions_frame.pack(fill=tk.X, pady=(0, 10))
        
        for i, solution_text in enumerate(solution["solutions"], 1):
            ttk.Label(solutions_frame, text=f"{i}. {solution_text}", font=("Arial", 10)).pack(anchor="w", pady=2)
        
        # Prevention
        prevention_frame = ttk.LabelFrame(self.content_frame, text="Prevention", padding=10)
        prevention_frame.pack(fill=tk.X, pady=(0, 10))
        
        for i, prevention_text in enumerate(solution["prevention"], 1):
            ttk.Label(prevention_frame, text=f"{i}. {prevention_text}", font=("Arial", 10)).pack(anchor="w", pady=2)
        
        # Back button
        ttk.Button(
            self.content_frame,
            text="← Back to Issues",
            command=lambda: self.show_infrastructure_troubleshooting()
        ).pack(pady=10)
    
    def get_issue_solution(self, issue: str) -> Dict:
        """Get solution for specific issue"""
        solutions = {
            "Terraform state is locked": {
                "diagnosis": "Terraform state is locked, likely by another process or team member",
                "solutions": [
                    "Check for running Terraform processes: `ps aux | grep terraform`",
                    "Use force unlock: `terraform force-unlock <lock-id>`",
                    "Check with team members if they're running Terraform",
                    "Verify no CI/CD pipeline is running Terraform"
                ],
                "prevention": [
                    "Use remote state with locking (S3 + DynamoDB)",
                    "Implement proper CI/CD pipeline coordination",
                    "Use Terraform workspaces for team collaboration"
                ]
            },
            "Resource already exists error": {
                "diagnosis": "Resource already exists in AWS but not in Terraform state",
                "solutions": [
                    "Import existing resource: `terraform import <resource_type>.<name> <resource_id>`",
                    "Check AWS console for existing resources",
                    "Use `terraform plan` to see what will be created",
                    "Consider using data sources instead of resources"
                ],
                "prevention": [
                    "Always use `terraform plan` before `terraform apply`",
                    "Keep Terraform state in sync with actual infrastructure",
                    "Use consistent naming conventions"
                ]
            }
        }
        
        return solutions.get(issue, {
            "diagnosis": "This is a complex issue that requires detailed analysis",
            "solutions": [
                "Gather more information about the specific error",
                "Check logs and monitoring data",
                "Consult documentation and best practices",
                "Contact support if needed"
            ],
            "prevention": [
                "Follow best practices and guidelines",
                "Implement proper monitoring and alerting",
                "Regular testing and validation",
                "Keep documentation up to date"
            ]
        })

class GUIInterface:
    """Main GUI interface for the intelligent agents"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Intelligent Infrastructure Agent")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Current project data
        self.current_project = None
        self.agents = {}
        if IntelligentTerraformAgent:
            self.agents["terraform"] = IntelligentTerraformAgent()
        
        self.create_interface()
    
    def create_interface(self):
        """Create the main interface"""
        # Main menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self.create_new_project)
        file_menu.add_command(label="Open Project", command=self.open_project)
        file_menu.add_command(label="Save Project", command=self.save_project)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Troubleshooting Assistant", command=self.open_troubleshooting)
        tools_menu.add_command(label="Scaling Plan Generator", command=self.open_scaling_plan)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.open_documentation)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="🚀 Intelligent Infrastructure Agent",
            font=("Arial", 20, "bold")
        ).pack()
        
        ttk.Label(
            header_frame,
            text="AI-powered infrastructure planning and deployment",
            font=("Arial", 12),
            foreground="gray"
        ).pack()
        
        # Welcome message
        welcome_frame = ttk.Frame(main_frame)
        welcome_frame.pack(fill=tk.BOTH, expand=True)
        
        welcome_text = """
Welcome to the Intelligent Infrastructure Agent!

This tool helps you design, plan, and deploy infrastructure with AI assistance.

🎯 What you can do:
• Create new infrastructure projects with guided requirements collection
• Generate Terraform code automatically
• Plan production scaling strategies
• Troubleshoot common infrastructure issues
• Optimize costs and performance

🚀 Get started by creating a new project or opening an existing one.
        """
        
        ttk.Label(
            welcome_frame,
            text=welcome_text,
            font=("Arial", 11),
            justify=tk.LEFT
        ).pack(pady=50)
        
        # Action buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(
            buttons_frame,
            text="🆕 Create New Project",
            command=self.create_new_project,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            buttons_frame,
            text="📂 Open Project",
            command=self.open_project
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            buttons_frame,
            text="🔧 Troubleshooting",
            command=self.open_troubleshooting
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            buttons_frame,
            text="📈 Scaling Plans",
            command=self.open_scaling_plan
        ).pack(side=tk.LEFT)
        
        # Status bar
        self.status_bar = ttk.Label(
            main_frame,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, pady=(20, 0))
    
    def create_new_project(self):
        """Create new project using wizard"""
        wizard = ProjectWizard(self.root, self.on_project_complete)
    
    def on_project_complete(self, project_data):
        """Handle project completion"""
        self.current_project = project_data
        self.status_bar.config(text=f"Project created: {project_data['project_type']}")
        
        # Show success message
        messagebox.showinfo(
            "Success",
            f"Project '{project_data['project_type']}' created successfully!\n\n"
            f"Cost estimate: ${project_data['response']['cost_estimate']}/month\n"
            f"Confidence: {project_data['response']['confidence'] * 100:.1f}%"
        )
    
    def open_project(self):
        """Open existing project"""
        file_path = filedialog.askopenfilename(
            title="Open Project",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    self.current_project = json.load(f)
                self.status_bar.config(text=f"Project loaded: {Path(file_path).stem}")
                messagebox.showinfo("Success", "Project loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load project: {e}")
    
    def save_project(self):
        """Save current project"""
        if not self.current_project:
            messagebox.showwarning("Warning", "No project to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Project",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.current_project, f, indent=2, default=str)
                self.status_bar.config(text=f"Project saved: {Path(file_path).stem}")
                messagebox.showinfo("Success", "Project saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save project: {e}")
    
    def open_troubleshooting(self):
        """Open troubleshooting interface"""
        TroubleshootingInterface(self.root)
    
    def open_scaling_plan(self):
        """Open scaling plan generator"""
        if not self.current_project:
            messagebox.showwarning("Warning", "Please create or load a project first")
            return
        
        # Generate scaling plan
        from interfaces.cli_interface import ProductionScalingPlanner, RequirementSet, Requirement
        
        planner = ProductionScalingPlanner()
        
        # Convert project data to requirements
        req_data = self.current_project.get("requirements", {})
        requirements = RequirementSet(
            project_name=req_data.get("project_name", "Unknown"),
            requirements=[],
            completeness_score=100.0
        )
        
        scaling_plan = planner.generate_scaling_plan(requirements)
        
        # Show scaling plan viewer
        ScalingPlanViewer(self.root, scaling_plan)
    
    def open_documentation(self):
        """Open documentation"""
        webbrowser.open("https://github.com/your-repo/docs")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
Intelligent Infrastructure Agent v1.0

AI-powered infrastructure planning and deployment tool.

Features:
• Automated Terraform code generation
• Intelligent requirement collection
• Production scaling planning
• Comprehensive troubleshooting
• Cost optimization

Built with Python, Tkinter, and AI reasoning engines.
        """
        
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main entry point"""
    app = GUIInterface()
    app.run()

if __name__ == "__main__":
    main()
