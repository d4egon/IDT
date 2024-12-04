import subprocess
from utilities.sandboxing import create_sandbox, cleanup_sandbox

class PythonHandler:
    def run_code(self, code_block, sandbox):
        try:
            sandbox_file = f"{sandbox}/temp_script.py"
            with open(sandbox_file, "w") as file:
                file.write(code_block)
            process = subprocess.run(
                ["python3", sandbox_file],
                capture_output=True,
                text=True,
            )
            if process.returncode == 0:
                return process.stdout
            else:
                return process.stderr
        except Exception as e:
            return f"Error running Python code: {e}"