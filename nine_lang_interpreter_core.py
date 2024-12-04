import logging
from language_handlers.python_handler import PythonHandler
from language_handlers.java_handler import JavaHandler
from language_handlers.c_handler import CHandler
from utilities.sandboxing import create_sandbox, cleanup_sandbox

class NineLangInterpreter:
    def __init__(self):
        self.handlers = {
            "python": PythonHandler(),
            "java": JavaHandler(),
            "c": CHandler(),
        }

    def execute(self, command, code_block=None):
        try:
            if command.startswith("$run_"):
                language = command.split("_")[1]
                handler = self.handlers.get(language)
                if handler:
                    sandbox = create_sandbox()
                    result = handler.run_code(code_block, sandbox)
                    cleanup_sandbox(sandbox)
                    return result
                else:
                    return f"Error: Language '{language}' is not supported."
            else:
                return f"Error: Unknown command '{command}'."
        except Exception as e:
            logging.error(f"Error executing command '{command}': {e}")
            return str(e)