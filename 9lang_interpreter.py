import os
import requests
import zipfile
import subprocess
import re
from tqdm import tqdm
import logging
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NineLangInterpreter:
    def __init__(self):
        self.environment = {}  # Tracks file placements
        self.undo_stack = []  # Stores undo actions
        self.redo_stack = []  # Stores redo actions
        self.command_map = {
            "->": self.handle_download,
            "<>": self.handle_unpack_or_zip,
            "<&>": self.handle_install,
            "validate": self.validate,
            "undo": self.undo,
            "redo": self.redo,
            "test": self.test_network,
            "%": self.delete_file,
            "@": self.handle_rotate,
            "==": self.handle_scale,
            "__": self.handle_flatten,
        }

    def execute(self, command):
        try:
            for key, handler in self.command_map.items():
                if key in command:
                    handler(command)
                    return
            logger.error("Unknown command")
        except Exception as e:
            logger.error(f"Error executing command '{command}': {e}")

    def sanitize_url(self, url):
        # Basic sanitization: check if URL matches a simple pattern
        if not re.match(r'^https?://[^\s/$.?#].[^\s]*$', url):
            raise ValueError("Invalid URL")
        return url

    def handle_download(self, command):
        _, ip, _, loc = command.split()
        ip = self.sanitize_url(ip)
        loc = tuple(map(int, loc.split(',')))
        filename = ip.split('/')[-1]
        filepath = os.path.join("downloads", filename)

        logger.info(f"Downloading {ip} to {filepath}...")
        response = requests.get(ip, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192

        with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
            with open(filepath, 'wb') as file:
                for data in response.iter_content(block_size):
                    file.write(data)
                    pbar.update(len(data))

        if response.status_code == 200:
            os.makedirs("downloads", exist_ok=True)
            self.environment[loc] = filepath
            self.undo_stack.append(("add", loc, filepath))
            logger.info(f"Downloaded and placed at {loc}.")
        else:
            logger.error(f"Failed to download: {response.status_code}")

    def handle_unpack_or_zip(self, command):
        parts = command.split()
        loc = tuple(map(int, parts[-1].split(',')))
        filepath = self.environment.get(loc)

        if "<>" in command and "high" not in command:
            logger.info(f"Unpacking {filepath}...")
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                unpack_path = os.path.join("downloads", "unpacked")
                os.makedirs(unpack_path, exist_ok=True)
                zip_ref.extractall(unpack_path)
            logger.info(f"Unpacked to {unpack_path}.")
        elif "high" in command:
            logger.info(f"Compressing {filepath} with high efficiency...")
            compressed_path = filepath + ".zip"
            with zipfile.ZipFile(compressed_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(filepath, arcname=os.path.basename(filepath))
            logger.info(f"Compressed to {compressed_path}.")

    def handle_install(self, command):
        _, ip, _, loc = command.split()
        ip = self.sanitize_url(ip)
        loc = tuple(map(int, loc.split(',')))
        logger.info(f"Installing {ip} to {loc}...")
        install_path = os.path.join("downloads", "installed")
        os.makedirs(install_path, exist_ok=True)
        logger.info(f"Installed at {install_path}.")

    def validate(self, command):
        _, _, rest = command.partition("validate")
        if rest.strip() in [item[0] for item in self.undo_stack]:
            logger.info("Validation successful.")
        else:
            logger.warning("Validation failed.")

    def undo(self):
        if self.undo_stack:
            action, loc, filepath = self.undo_stack.pop()
            if action == "add" and loc in self.environment:
                if os.path.exists(filepath):
                    os.remove(filepath)
                del self.environment[loc]
                logger.info(f"Undone placement at {loc}.")
                self.redo_stack.append(("add", loc, filepath))
        else:
            logger.warning("Nothing to undo.")

    def redo(self):
        if self.redo_stack:
            action, loc, filepath = self.redo_stack.pop()
            if action == "add" and loc not in self.environment:
                shutil.copy(filepath, os.path.join("downloads", os.path.basename(filepath)))
                self.environment[loc] = filepath
                self.undo_stack.append(("add", loc, filepath))
                logger.info(f"Redone placement at {loc}.")
        else:
            logger.warning("Nothing to redo.")

    def test_network(self, command):
        _, ip = command.split()
        logger.info(f"Testing connection to {ip}...")
        try:
            subprocess.run(["ping", "-c", "1", ip], check=True)
            logger.info(f"{ip} is reachable.")
        except subprocess.CalledProcessError:
            logger.error(f"Failed to reach {ip}.")

    def delete_file(self, command):
        _, ip, _, loc = command.split()
        loc = tuple(map(int, loc.split(',')))
        filepath = self.environment.get(loc)
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
            del self.environment[loc]
            logger.info(f"Deleted file at {loc}.")
        else:
            logger.warning(f"No file to delete at {loc}.")

    def handle_rotate(self, command):
        _, structure, _, angle = command.split()
        logger.info(f"Rotating {structure} by {angle} degrees.")

    def handle_scale(self, command):
        _, scale_type, _, factor = command.split()
        logger.info(f"Scaling {scale_type} by a factor of {factor}.")

    def handle_flatten(self, command):
        _, target, _, direction = command.split()
        logger.info(f"Flattening {target} along {direction}.")

# Example usage
interpreter = NineLangInterpreter()
interpreter.execute("$https://example.com/file.zip -> 0,1,0")
interpreter.execute("8 validate $https://example.com/file.zip -> 0,1,0")
