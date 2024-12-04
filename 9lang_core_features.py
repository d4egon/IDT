class NineLangCore:
    def __init__(self):
        self.stacks = {}  # Dictionary to hold all stacks

    def create_stack(self, name, content=None):
        if name in self.stacks:
            return f"Error: Stack '{name}' already exists."
        self.stacks[name] = {
            "content": content or [],
            "metadata": {
                "type": "default",
                "description": "A basic stack."
            }
        }
        return f"Stack '{name}' created successfully."

    def view_stack(self, name):
        if name not in self.stacks:
            return f"Error: Stack '{name}' does not exist."
        stack = self.stacks[name]
        return {
            "content": stack["content"],
            "metadata": stack["metadata"]
        }

    def split_stack(self, name):
        if name not in self.stacks:
            return f"Error: Stack '{name}' does not exist."
        original_stack = self.stacks[name]["content"]
        if not original_stack:
            return f"Error: Cannot split an empty stack '{name}'."
        mid = len(original_stack) // 2
        self.stacks[f"{name}_part1"] = {
            "content": original_stack[:mid],
            "metadata": {
                "type": "split",
                "description": f"First part of split from '{name}'."
            }
        }
        self.stacks[f"{name}_part2"] = {
            "content": original_stack[mid:],
            "metadata": {
                "type": "split",
                "description": f"Second part of split from '{name}'."
            }
        }
        del self.stacks[name]
        return f"Stack '{name}' split into '{name}_part1' and '{name}_part2'."

    def fuse_stacks(self, name1, name2):
        if name1 not in self.stacks or name2 not in self.stacks:
            return f"Error: One or both stacks '{name1}' and '{name2}' do not exist."
        self.stacks[f"{name1}_{name2}_fused"] = {
            "content": self.stacks[name1]["content"] + self.stacks[name2]["content"],
            "metadata": {
                "type": "fused",
                "description": f"Fusion of stacks '{name1}' and '{name2}'."
            }
        }
        del self.stacks[name1]
        del self.stacks[name2]
        return f"Stacks '{name1}' and '{name2}' fused into '{name1}_{name2}_fused'."

    def flatten_stack(self, name, direction=None):
        if name not in self.stacks:
            return f"Error: Stack '{name}' does not exist."
        stack_content = self.stacks[name]["content"]
        if not isinstance(stack_content, list):
            return f"Error: Stack '{name}' is not a list and cannot be flattened."
        if direction:
            return f"Flattening stack '{name}' along direction {direction}."
        return f"Flattened stack '{name}' into: {stack_content}"

    def scale_stack(self, name, factor):
        if name not in self.stacks:
            return f"Error: Stack '{name}' does not exist."
        stack_content = self.stacks[name]["content"]
        if not isinstance(stack_content, list):
            return f"Error: Stack '{name}' cannot be scaled."
        scaled_stack = [element * factor for element in stack_content if isinstance(element, (int, float))]
        self.stacks[name]["content"] = scaled_stack
        self.stacks[name]["metadata"]["description"] += f" Scaled by a factor of {factor}."
        return f"Stack '{name}' scaled by a factor of {factor}."

    def prepare_for_visualization(self):
        visualization_data = {
            name: {
                "content": stack["content"],
                "metadata": stack["metadata"]
            }
            for name, stack in self.stacks.items()
        }
        return visualization_data

# Example Usage
core = NineLangCore()
print(core.create_stack("alpha", [1, 2, 3, 4]))
print(core.split_stack("alpha"))
print(core.fuse_stacks("alpha_part1", "alpha_part2"))
print(core.scale_stack("alpha_part1_alpha_part2_fused", 2))
print(core.flatten_stack("alpha_part1_alpha_part2_fused"))
print(core.prepare_for_visualization())
