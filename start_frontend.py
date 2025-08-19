#!/usr/bin/env python3
"""
Frontend startup script for the Adaptive AI Assistant
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_node_installed():
    """Check if Node.js is installed."""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js not found. Please install Node.js to run the frontend.")
    return False

def check_npm_installed():
    """Check if npm is installed."""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ npm not found. Please install npm to run the frontend.")
    return False

def install_dependencies():
    """Install frontend dependencies."""
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    os.chdir(frontend_dir)
    
    print("📦 Installing frontend dependencies...")
    try:
        result = subprocess.run(['npm', 'install'], check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_frontend():
    """Start the frontend development server."""
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    os.chdir(frontend_dir)
    
    print("🚀 Starting frontend development server...")
    print("📱 Frontend will be available at: https://work-1-znvqiaywdzthncvd.prod-runtime.all-hands.dev")
    print("🔗 Make sure the backend API is running on port 8000")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        # Start the development server
        subprocess.run(['npm', 'run', 'start'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start frontend: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped by user")
        return True

def main():
    """Main function."""
    print("🎨 Adaptive AI Assistant - Frontend Startup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_node_installed():
        return 1
    
    if not check_npm_installed():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    # Start frontend
    if not start_frontend():
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())