import os
import sys
import time
import webbrowser
import subprocess
import socket

# Ensure 'no_color' is set in the environment variables to prevent KeyError
os.environ['DJANGO_NO_COLOR'] = '1'

# Set Django settings module if not already set
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'software.settings'

# Define the absolute path to your Django project (adjust this to your project path)
project_dir = r"E:\gym software\software"  # Path where manage.py is located

# Add project directory to sys.path to avoid module import issues
sys.path.insert(0, project_dir)

# Change the current working directory to the project folder where manage.py is located
os.chdir(project_dir)

# Define the server address
server_address = "http://127.0.0.1:8000"

# Function to check if the server is running
def is_server_running(host="127.0.0.1", port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex((host, port)) == 0

try:
    # Start the Django server as a background process
    process = subprocess.Popen(["python", "manage.py", "runserver"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait and check until the server is up
    for _ in range(10):  # Retry up to 10 times (adjust if needed)
        if is_server_running():
            webbrowser.open(server_address)  # Open the URL in the default browser
            print(f"Server is running at {server_address}")
            break
        time.sleep(1)  # Wait 1 second before retrying
    else:
        print("Failed to detect server start. Please open the browser manually.")

except Exception as e:
    print(f"Error executing Django command: {e}")
    sys.exit(1)
