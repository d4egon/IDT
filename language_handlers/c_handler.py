import subprocess
from utilities.sandboxing import create_sandbox, cleanup_sandbox

class CHandler:
    def run_code(self, code_block, sandbox):
        try:
            sandbox_file = f"{sandbox}/temp_program.c"
            output_file = f"{sandbox}/temp_program"

            with open(sandbox_file, "w") as file:
                file.write(code_block)

            compile_process = subprocess.run(
                ["gcc", sandbox_file, "-o", output_file], capture_output=True, text=True
            )

            if compile_process.returncode == 0:
                run_process = subprocess.run(
                    [output_file], capture_output=True, text=True
                )
                return run_process.stdout if run_process.returncode == 0 else run_process.stderr
            else:
                return compile_process.stderr
        except Exception as e:
            return f"Error running C code: {e}"