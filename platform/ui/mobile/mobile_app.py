"""
Mobile interface for the AI-AH Multi-Agent Infrastructure Intelligence Platform.

This module provides a mobile-friendly interface using Kivy for cross-platform
mobile applications.
"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.switch import Switch
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
import json
import threading
from datetime import datetime
from typing import Dict, Any, Optional

kivy.require('2.1.0')


class LoginScreen(Screen):
    """Login screen for the mobile app."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the login UI."""
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # App title
        title = Label(
            text='AI-AH Platform',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        layout.add_widget(title)
        
        # Username input
        self.username_input = TextInput(
            hint_text='Username',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.username_input)
        
        # Password input
        self.password_input = TextInput(
            hint_text='Password',
            multiline=False,
            password=True,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.password_input)
        
        # Login button
        login_btn = Button(
            text='Login',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1)
        )
        login_btn.bind(on_press=self.login)
        layout.add_widget(login_btn)
        
        # Demo login button
        demo_btn = Button(
            text='Demo Login',
            size_hint_y=None,
            height=50,
            background_color=(0.3, 0.7, 0.3, 1)
        )
        demo_btn.bind(on_press=self.demo_login)
        layout.add_widget(demo_btn)
        
        self.add_widget(layout)
    
    def login(self, instance):
        """Handle login."""
        username = self.username_input.text
        password = self.password_input.text
        
        if not username or not password:
            self.show_error("Please enter username and password")
            return
        
        # Make login request
        self.make_login_request(username, password)
    
    def demo_login(self, instance):
        """Demo login with default credentials."""
        self.username_input.text = "admin"
        self.password_input.text = "admin123"
        self.login(instance)
    
    def make_login_request(self, username: str, password: str):
        """Make login API request."""
        url = "http://localhost:8000/api/v1/auth/login"
        data = json.dumps({
            "username": username,
            "password": password
        })
        headers = {"Content-Type": "application/json"}
        
        def on_success(request, result):
            app = App.get_running_app()
            app.auth_token = result.get("access_token")
            app.current_user = result.get("user")
            app.sm.current = "dashboard"
        
        def on_failure(request, result):
            self.show_error("Login failed: Invalid credentials")
        
        UrlRequest(url, on_success=on_success, on_failure=on_failure,
                  req_body=data, req_headers=headers)
    
    def show_error(self, message: str):
        """Show error popup."""
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()


class DashboardScreen(Screen):
    """Dashboard screen showing platform overview."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup the dashboard UI."""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        title = Label(text='Dashboard', font_size='20sp')
        logout_btn = Button(text='Logout', size_hint_x=None, width=100)
        logout_btn.bind(on_press=self.logout)
        header.add_widget(title)
        header.add_widget(logout_btn)
        layout.add_widget(header)
        
        # Stats grid
        stats_grid = GridLayout(cols=2, size_hint_y=None, height=200, spacing=10)
        
        self.active_agents_label = Label(
            text='Active Agents\n5',
            font_size='16sp',
            halign='center'
        )
        self.running_tasks_label = Label(
            text='Running Tasks\n12',
            font_size='16sp',
            halign='center'
        )
        self.alerts_label = Label(
            text='Alerts\n3',
            font_size='16sp',
            halign='center'
        )
        self.success_rate_label = Label(
            text='Success Rate\n98.5%',
            font_size='16sp',
            halign='center'
        )
        
        stats_grid.add_widget(self.active_agents_label)
        stats_grid.add_widget(self.running_tasks_label)
        stats_grid.add_widget(self.alerts_label)
        stats_grid.add_widget(self.success_rate_label)
        layout.add_widget(stats_grid)
        
        # Agent buttons
        agents_layout = BoxLayout(orientation='vertical', spacing=10)
        
        terraform_btn = Button(
            text='Terraform Agent\nInfrastructure Provisioning',
            size_hint_y=None,
            height=80,
            background_color=(0.2, 0.6, 1, 1)
        )
        terraform_btn.bind(on_press=lambda x: self.switch_to_agent('terraform'))
        
        ansible_btn = Button(
            text='Ansible Agent\nConfiguration Management',
            size_hint_y=None,
            height=80,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        ansible_btn.bind(on_press=lambda x: self.switch_to_agent('ansible'))
        
        k8s_btn = Button(
            text='Kubernetes Agent\nContainer Orchestration',
            size_hint_y=None,
            height=80,
            background_color=(0.8, 0.2, 0.8, 1)
        )
        k8s_btn.bind(on_press=lambda x: self.switch_to_agent('kubernetes'))
        
        security_btn = Button(
            text='Security Agent\nSecurity & Compliance',
            size_hint_y=None,
            height=80,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        security_btn.bind(on_press=lambda x: self.switch_to_agent('security'))
        
        monitoring_btn = Button(
            text='Monitoring Agent\nMonitoring & Observability',
            size_hint_y=None,
            height=80,
            background_color=(0.8, 0.8, 0.2, 1)
        )
        monitoring_btn.bind(on_press=lambda x: self.switch_to_agent('monitoring'))
        
        agents_layout.add_widget(terraform_btn)
        agents_layout.add_widget(ansible_btn)
        agents_layout.add_widget(k8s_btn)
        agents_layout.add_widget(security_btn)
        agents_layout.add_widget(monitoring_btn)
        
        layout.add_widget(agents_layout)
        
        self.add_widget(layout)
    
    def load_data(self):
        """Load dashboard data."""
        app = App.get_running_app()
        if app.auth_token:
            self.make_status_request()
    
    def make_status_request(self):
        """Make status API request."""
        url = "http://localhost:8000/api/v1/platform/status"
        headers = {"Authorization": f"Bearer {App.get_running_app().auth_token}"}
        
        def on_success(request, result):
            self.update_stats(result.get("data", {}))
        
        def on_failure(request, result):
            print("Failed to load status")
        
        UrlRequest(url, on_success=on_success, on_failure=on_failure,
                  req_headers=headers)
    
    def update_stats(self, data: Dict[str, Any]):
        """Update dashboard statistics."""
        self.active_agents_label.text = f'Active Agents\n{data.get("agents_count", 0)}'
        self.running_tasks_label.text = f'Running Tasks\n{data.get("active_tasks", 0)}'
        self.alerts_label.text = f'Alerts\n{data.get("alerts", 0)}'
        self.success_rate_label.text = f'Success Rate\n{data.get("success_rate", 98.5)}%'
    
    def switch_to_agent(self, agent_type: str):
        """Switch to agent screen."""
        app = App.get_running_app()
        app.current_agent = agent_type
        app.sm.current = "agent"
    
    def logout(self, instance):
        """Handle logout."""
        app = App.get_running_app()
        app.auth_token = None
        app.current_user = None
        app.sm.current = "login"


class AgentScreen(Screen):
    """Agent interaction screen."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the agent UI."""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.title_label = Label(text='Agent', font_size='20sp')
        back_btn = Button(text='Back', size_hint_x=None, width=100)
        back_btn.bind(on_press=self.go_back)
        header.add_widget(self.title_label)
        header.add_widget(back_btn)
        layout.add_widget(header)
        
        # Requirements input
        self.requirements_input = TextInput(
            hint_text='Enter your requirements...',
            multiline=True,
            size_hint_y=None,
            height=150
        )
        layout.add_widget(self.requirements_input)
        
        # Action buttons
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        analyze_btn = Button(text='Analyze', background_color=(0.2, 0.6, 1, 1))
        analyze_btn.bind(on_press=self.analyze_requirements)
        
        generate_btn = Button(text='Generate', background_color=(0.2, 0.8, 0.2, 1))
        generate_btn.bind(on_press=self.generate_plan)
        
        execute_btn = Button(text='Execute', background_color=(0.8, 0.2, 0.2, 1))
        execute_btn.bind(on_press=self.execute_plan)
        
        buttons_layout.add_widget(analyze_btn)
        buttons_layout.add_widget(generate_btn)
        buttons_layout.add_widget(execute_btn)
        layout.add_widget(buttons_layout)
        
        # Results area
        self.results_scroll = ScrollView()
        self.results_label = Label(
            text='Results will appear here...',
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        self.results_scroll.add_widget(self.results_label)
        layout.add_widget(self.results_scroll)
        
        self.add_widget(layout)
    
    def on_enter(self):
        """Called when screen is entered."""
        app = App.get_running_app()
        if app.current_agent:
            agent_names = {
                'terraform': 'Terraform Agent',
                'ansible': 'Ansible Agent',
                'kubernetes': 'Kubernetes Agent',
                'security': 'Security Agent',
                'monitoring': 'Monitoring Agent'
            }
            self.title_label.text = agent_names.get(app.current_agent, 'Agent')
    
    def go_back(self, instance):
        """Go back to dashboard."""
        App.get_running_app().sm.current = "dashboard"
    
    def analyze_requirements(self, instance):
        """Analyze requirements."""
        requirements = self.requirements_input.text
        if not requirements.strip():
            self.show_error("Please enter requirements")
            return
        
        app = App.get_running_app()
        if not app.current_agent:
            return
        
        self.make_analyze_request(app.current_agent, requirements)
    
    def generate_plan(self, instance):
        """Generate plan."""
        requirements = self.requirements_input.text
        if not requirements.strip():
            self.show_error("Please enter requirements")
            return
        
        app = App.get_running_app()
        if not app.current_agent:
            return
        
        # First analyze, then generate
        self.make_analyze_and_generate_request(app.current_agent, requirements)
    
    def execute_plan(self, instance):
        """Execute plan."""
        self.show_error("Plan execution not implemented in mobile demo")
    
    def make_analyze_request(self, agent_type: str, requirements: str):
        """Make analyze API request."""
        url = f"http://localhost:8000/api/v1/agents/{agent_type}/analyze"
        headers = {"Authorization": f"Bearer {App.get_running_app().auth_token}"}
        data = json.dumps(requirements)
        
        def on_success(request, result):
            self.show_results("Analysis Results", result)
        
        def on_failure(request, result):
            self.show_error("Analysis failed")
        
        UrlRequest(url, on_success=on_success, on_failure=on_failure,
                  req_body=data, req_headers=headers)
    
    def make_analyze_and_generate_request(self, agent_type: str, requirements: str):
        """Make analyze and generate API request."""
        # First analyze
        analyze_url = f"http://localhost:8000/api/v1/agents/{agent_type}/analyze"
        headers = {"Authorization": f"Bearer {App.get_running_app().auth_token}"}
        data = json.dumps(requirements)
        
        def on_analyze_success(request, result):
            # Then generate plan
            generate_url = f"http://localhost:8000/api/v1/agents/{agent_type}/generate"
            generate_data = json.dumps(result)
            
            def on_generate_success(request, result):
                self.show_results("Generated Plan", result)
            
            def on_generate_failure(request, result):
                self.show_error("Plan generation failed")
            
            UrlRequest(generate_url, on_success=on_generate_success,
                      on_failure=on_generate_failure, req_body=generate_data,
                      req_headers=headers)
        
        def on_analyze_failure(request, result):
            self.show_error("Analysis failed")
        
        UrlRequest(analyze_url, on_success=on_analyze_success,
                  on_failure=on_analyze_failure, req_body=data,
                  req_headers=headers)
    
    def show_results(self, title: str, data: Dict[str, Any]):
        """Show results in a popup."""
        content = ScrollView()
        result_label = Label(
            text=json.dumps(data, indent=2),
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        content.add_widget(result_label)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.9, 0.8)
        )
        popup.open()
    
    def show_error(self, message: str):
        """Show error popup."""
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()


class AIAHMobileApp(App):
    """Main mobile application class."""
    
    def build(self):
        """Build the application."""
        self.title = "AI-AH Platform"
        self.auth_token = None
        self.current_user = None
        self.current_agent = None
        
        # Create screen manager
        self.sm = ScreenManager()
        
        # Add screens
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(DashboardScreen(name='dashboard'))
        self.sm.add_widget(AgentScreen(name='agent'))
        
        return self.sm
    
    def on_start(self):
        """Called when app starts."""
        # Check if already logged in
        if self.auth_token:
            self.sm.current = "dashboard"
        else:
            self.sm.current = "login"


if __name__ == '__main__':
    AIAHMobileApp().run()
