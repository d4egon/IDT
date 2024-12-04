import os
import tempfile

class Sandboxing:
    @staticmethod
    def create_sandbox():
        return tempfile.mkdtemp()

    @staticmethod
    def cleanup_sandbox(sandbox_path):
        if os.path.exists(sandbox_path):
            for root, dirs, files in os.walk(sandbox_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(sandbox_path)