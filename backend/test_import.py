import sys
import os
print("Current directory:", os.getcwd())
print("Python executable:", sys.executable)
try:
    from main import app
    print("Main app imported successfully!")
    print("App:", app)
except Exception as e:
    print(f"Error importing main: {e}")
    import traceback
    traceback.print_exc()
