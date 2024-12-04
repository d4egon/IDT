import threading

class AdvancedOperations:
    def __init__(self, stacks):
        self.stacks = stacks

    def parallel_execute(self, commands):
        results = {}
        threads = []

        def execute_command(index, command):
            try:
                if command.startswith("rotate"):
                    _, structure_name, angle = command.split()
                    results[index] = self.rotate_perspective(structure_name, angle)
                elif command.startswith("snake"):
                    _, stack_name = command.split()
                    if stack_name in self.stacks:
                        results[index] = self.snaking_movement(self.stacks[stack_name]["content"])
                    else:
                        results[index] = f"Error: Stack '{stack_name}' does not exist."
                else:
                    results[index] = f"Unknown command: {command}"
            except Exception as e:
                results[index] = f"Error: {e}"

        for i, command in enumerate(commands):
            thread = threading.Thread(target=execute_command, args=(i, command))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return "\n".join(results[i] for i in sorted(results))

    def snaking_movement(self, items):
        if not isinstance(items, list):
            return "Error: Can only traverse lists."
        traversed = []
        for i, item in enumerate(items):
            if i % 2 == 0:
                traversed.append(f"Traversed: {item}")
            else:
                traversed.append(f"Reversed Traversed: {item}")
        return "\n".join(traversed)

    def rotate_perspective(self, structure_name, angle):
        if structure_name not in self.stacks:
            return f"Error: Structure '{structure_name}' does not exist."
        try:
            angle = int(angle)
            self.stacks[structure_name]["metadata"]["rotation"] = angle
            return f"Structure '{structure_name}' rotated by {angle} degrees."
        except ValueError:
            return "Error: Invalid angle."

# Example Usage
stacks = {
    "alpha": {
        "content": [1, 2, 3, 4],
        "metadata": {"type": "default", "description": "A test stack."}
    }
}

operations = AdvancedOperations(stacks)
print(operations.parallel_execute([
    "rotate alpha 45",
    "snake alpha",
    "rotate beta 90"
]))
