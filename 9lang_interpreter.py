import os
import requests
import zipfile
import shutil

class NineLangInterpreter:
    def __init__(self):
        self.environment = {}
        self.undo_stack = []
        self.redo_stack = []

    def execute(self, command):
        try:
            if "->" in command:
                self.handle_download(command)
            elif "<>" in command:
                self.handle_unpack_or_zip(command)
            elif "<&>" in command:
                self.handle_install(command)
            elif "validate" in command:
                self.validate(command)
            elif "undo" in command:
                self.undo()
            elif "redo" in command:
                self.redo()
            elif "test" in command:
                self.test_network(command)
            elif "%" in command:
                self.delete_file(command)
            elif "@" in command:
                self.handle_rotate(command)
            elif "==" in command:
                self.handle_scale(command)
            elif "__" in command:
                self.handle_flatten(command)
            else:
                print("Unknown command")
        except Exception as e:
            print(f"Error executing command: {e}")

    def handle_download(self, command):
        _, ip, _, loc = command.split()
        loc = tuple(map(int, loc.split(',')))
        filename = ip.split('/')[-1]
        filepath = os.path.join("downloads", filename)

        print(f"Downloading {ip} to {filepath}...")
        response = requests.get(ip, stream=True)
        if response.status_code == 200:
            os.makedirs("downloads", exist_ok=True)
            with open(filepath, 'wb') as file:
                file.write(response.content)
            self.environment[loc] = filepath
            self.undo_stack.append(("add", loc))
            print(f"Downloaded and placed at {loc}.")
        else:
            print(f"Failed to download: {response.status_code}")

    def handle_unpack_or_zip(self, command):
        parts = command.split()
        ip = parts[1]
        loc = tuple(map(int, parts[-1].split(',')))
        filepath = self.environment.get(loc)

        if "<>" in command and "high" not in command:
            print(f"Unpacking {filepath}...")
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                unpack_path = os.path.join("downloads", "unpacked")
                os.makedirs(unpack_path, exist_ok=True)
                zip_ref.extractall(unpack_path)
            print(f"Unpacked to {unpack_path}.")
        elif "high" in command:
            print(f"Compressing {filepath} with high efficiency...")
            compressed_path = filepath + ".zip"
            with zipfile.ZipFile(compressed_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(filepath, arcname=os.path.basename(filepath))
            print(f"Compressed to {compressed_path}.")

    def handle_install(self, command):
        _, ip, _, loc = command.split()
        loc = tuple(map(int, loc.split(',')))
        print(f"Installing {ip} to {loc}...")
        filepath = os.path.join("downloads", "installed", loc)
        os.makedirs(filepath, exist_ok=True)
        print(f"Installed at {filepath}.")

    def validate(self, command):
        _, _, rest = command.partition("validate")
        if rest.strip() in self.undo_stack:
            print("Validation successful.")
        else:
            print("Validation failed.")

    def undo(self):
        if self.undo_stack:
            action, loc = self.undo_stack.pop()
            if action == "add" and loc in self.environment:
                filepath = self.environment.pop(loc)
                if os.path.exists(filepath):
                    os.remove(filepath)
                print(f"Undone placement at {loc}.")
                self.redo_stack.append(("add", loc))
        else:
            print("Nothing to undo.")

    def redo(self):
        if self.redo_stack:
            action, loc = self.redo_stack.pop()
            if action == "add" and loc not in self.environment:
                print(f"Redo functionality for placement at {loc} is pending.")
        else:
            print("Nothing to redo.")

    def test_network(self, command):
        _, ip = command.split()
        print(f"Testing connection to {ip}...")
        response = os.system(f"ping -c 1 {ip}")
        if response == 0:
            print(f"{ip} is reachable.")
        else:
            print(f"Failed to reach {ip}.")

    def delete_file(self, command):
        _, ip, _, loc = command.split()
        loc = tuple(map(int, loc.split(',')))
        filepath = self.environment.get(loc)
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
            print(f"Deleted file at {loc}.")
        else:
            print(f"No file to delete at {loc}.")

    def handle_rotate(self, command):
        _, structure, _, angle = command.split()
        print(f"Rotating {structure} by {angle} degrees.")

    def handle_scale(self, command):
        _, scale_type, _, factor = command.split()
        print(f"Scaling {scale_type} by a factor of {factor}.")

    def handle_flatten(self, command):
        _, target, _, direction = command.split()
        print(f"Flattening {target} along {direction}.")

# Example usage
interpreter = NineLangInterpreter()
interpreter.execute("$https://example.com/file.zip -> 0,1,0")
interpreter.execute("8 validate $https://example.com/file.zip -> 0,1,0")
