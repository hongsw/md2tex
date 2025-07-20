import sys
import os
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")
print(f"sys.argv: {sys.argv}")

# Try importing md2tex
try:
    import md2tex
    print("md2tex imported successfully")
except Exception as e:
    print(f"Error importing md2tex: {e}")

# Try running the command
import subprocess
result = subprocess.run([sys.executable, "md2tex.py", "test.md", "-c", "-o", "test.tex"], 
                       capture_output=True, text=True)
print(f"Return code: {result.returncode}")
print(f"Stdout: {result.stdout}")
print(f"Stderr: {result.stderr}")