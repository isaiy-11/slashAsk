import subprocess
import sys
import time
import webbrowser

def main():
    print("Starting FastAPI backend...")
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"]
    )

    print("Starting Streamlit frontend...")
    frontend = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "ui/streamlit_app.py", "--server.headless=false"]
    )

    print("Waiting for Streamlit to start and open the browser...")

    try:
        # Keep the script running
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
