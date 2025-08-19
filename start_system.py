#!/usr/bin/env python3
"""
Complete system startup script for the Adaptive AI Assistant
Starts both backend API and frontend simultaneously
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path
from dotenv import load_dotenv

def check_environment():
    """Check if all required environment variables are set."""
    load_dotenv()
    
    required_vars = ['PERPLEXITY_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   • {var}")
        print("\nPlease create a .env file with the required variables.")
        return False
    
    print("✅ Environment variables configured")
    return True

def install_python_dependencies():
    """Install Python dependencies."""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Python dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        return False

def install_frontend_dependencies():
    """Install frontend dependencies."""
    frontend_dir = Path(__file__).parent / "frontend"
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    print("📦 Installing frontend dependencies...")
    try:
        subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True, capture_output=True)
        print("✅ Frontend dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install frontend dependencies: {e}")
        return False
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js and npm.")
        return False

def start_backend():
    """Start the backend API server."""
    print("🚀 Starting backend API server...")
    try:
        # Start the FastAPI server
        process = subprocess.Popen([
            sys.executable, '-m', 'uvicorn', 
            'api.main:app', 
            '--host', '0.0.0.0', 
            '--port', '8000',
            '--reload'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment to check if it started successfully
        time.sleep(3)
        if process.poll() is None:
            print("✅ Backend API server started on http://localhost:8000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the frontend development server."""
    frontend_dir = Path(__file__).parent / "frontend"
    
    print("🎨 Starting frontend development server...")
    try:
        # Start the Vite development server
        process = subprocess.Popen([
            'npm', 'run', 'start'
        ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment to check if it started successfully
        time.sleep(5)
        if process.poll() is None:
            print("✅ Frontend server started on https://work-1-znvqiaywdzthncvd.prod-runtime.all-hands.dev")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Frontend failed to start:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return None

def monitor_processes(backend_process, frontend_process):
    """Monitor both processes and handle shutdown."""
    try:
        while True:
            # Check if processes are still running
            if backend_process and backend_process.poll() is not None:
                print("❌ Backend process died unexpectedly")
                break
            
            if frontend_process and frontend_process.poll() is not None:
                print("❌ Frontend process died unexpectedly")
                break
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n🛑 Shutting down system...")
        
        # Terminate processes gracefully
        if backend_process:
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
                print("✅ Backend server stopped")
            except subprocess.TimeoutExpired:
                backend_process.kill()
                print("🔪 Backend server force killed")
        
        if frontend_process:
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=5)
                print("✅ Frontend server stopped")
            except subprocess.TimeoutExpired:
                frontend_process.kill()
                print("🔪 Frontend server force killed")
        
        print("👋 System shutdown complete")

def main():
    """Main function."""
    print("🚀 Adaptive AI Assistant - Complete System Startup")
    print("=" * 60)
    print("Features:")
    print("• Dynamic personality profiling")
    print("• Adaptive task extraction") 
    print("• Personalized responses")
    print("• Generative React UI")
    print("• Real-time WebSocket communication")
    print("=" * 60)
    
    # Check environment
    if not check_environment():
        return 1
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_python_dependencies():
        return 1
    
    if not install_frontend_dependencies():
        return 1
    
    print("\n🚀 Starting services...")
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return 1
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        if backend_process:
            backend_process.terminate()
        return 1
    
    print("\n" + "=" * 60)
    print("🎉 System started successfully!")
    print("📱 Frontend: https://work-1-znvqiaywdzthncvd.prod-runtime.all-hands.dev")
    print("🔗 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    print("=" * 60)
    print("Press Ctrl+C to stop all services")
    print("=" * 60)
    
    # Monitor processes
    monitor_processes(backend_process, frontend_process)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())