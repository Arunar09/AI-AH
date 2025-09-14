#!/usr/bin/env python3
"""
Interface Launcher
Allows users to choose between CLI and GUI interfaces
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Main launcher function"""
    print("🚀 Intelligent Infrastructure Agent Interface Launcher")
    print("=" * 60)
    
    print("\n📋 Available Interfaces:")
    print("1. CLI Interface - Command-line interface for power users")
    print("2. GUI Interface - Visual interface for interactive planning")
    print("3. Web Interface - Modern web-based interface with dropdown options")
    print("4. All Interfaces - Launch CLI, GUI, and Web interfaces")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\n💬 Select interface (0-4): ").strip()
            
            if choice == "1":
                print("\n🚀 Launching CLI Interface...")
                subprocess.run([sys.executable, "interfaces/cli_interface.py", "--interactive"])
                break
                
            elif choice == "2":
                print("\n🚀 Launching GUI Interface...")
                subprocess.run([sys.executable, "interfaces/gui_interface.py"])
                break
                
            elif choice == "3":
                print("\n🚀 Launching Web Interface...")
                print("📱 Web interface will be available at: http://localhost:5000")
                subprocess.run([sys.executable, "interfaces/web_interface.py"])
                break
                
            elif choice == "4":
                print("\n🚀 Launching all interfaces...")
                print("CLI will open in this terminal, GUI and Web will open in new windows")
                print("📱 Web interface will be available at: http://localhost:5000")
                
                # Launch GUI in background
                if os.name == 'nt':  # Windows
                    subprocess.Popen([sys.executable, "interfaces/gui_interface.py"], 
                                   creationflags=subprocess.CREATE_NEW_CONSOLE)
                    subprocess.Popen([sys.executable, "interfaces/web_interface.py"], 
                                   creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:  # Unix/Linux/Mac
                    subprocess.Popen([sys.executable, "interfaces/gui_interface.py"])
                    subprocess.Popen([sys.executable, "interfaces/web_interface.py"])
                
                # Launch CLI in current terminal
                subprocess.run([sys.executable, "interfaces/cli_interface.py", "--interactive"])
                break
                
            elif choice == "0":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please select 0-3.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
