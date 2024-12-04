import socket
import json
import re

class NetworkingHandler:
    def __init__(self):
        self.connections = {}

    def validate_ip(self, ip_address):
        ip_pattern = re.compile(
            r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        )
        return ip_pattern.match(ip_address) is not None

    def tether_cube(self, ip_address):
        if not self.validate_ip(ip_address):
            return f"Error: Invalid IP address '{ip_address}'."

        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.settimeout(5)  # Security: Set connection timeout
            connection.connect((ip_address, 9000))
            self.connections[ip_address] = connection
            return f"Successfully tethered to cube at {ip_address}."
        except Exception as e:
            return f"Failed to tether to cube at {ip_address}: {e}"

    def sync_cube(self, ip_address, data=None):
        if ip_address not in self.connections:
            return f"Error: No active connection to cube at {ip_address}. Use 'tether_cube' first."

        connection = self.connections[ip_address]
        payload = {
            "type": "sync",
            "data": data or {"example_key": "example_value"}
        }

        try:
            message = json.dumps(payload)
            connection.sendall(message.encode('utf-8'))
            response = connection.recv(4096).decode('utf-8')
            remote_data = json.loads(response)
            return f"Synchronization successful with data: {remote_data}"
        except Exception as e:
            return f"Synchronization failed: {e}"

    def test_cube(self, ip_address):
        if not self.validate_ip(ip_address):
            return f"Error: Invalid IP address '{ip_address}'."

        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(3)
            test_socket.connect((ip_address, 9000))
            test_socket.close()
            return f"Cube at {ip_address} is reachable."
        except Exception as e:
            return f"Cube at {ip_address} is unreachable: {e}"

    def disconnect_cube(self, ip_address):
        if ip_address in self.connections:
            try:
                self.connections[ip_address].close()
                del self.connections[ip_address]
                return f"Disconnected from cube at {ip_address}."
            except Exception as e:
                return f"Error disconnecting from cube at {ip_address}: {e}"
        return f"Error: No active connection to cube at {ip_address}."

# Example Usage
handler = NetworkingHandler()
print(handler.test_cube("192.168.1.10"))
print(handler.tether_cube("192.168.1.10"))
print(handler.sync_cube("192.168.1.10", {"file": "example.txt"}))
print(handler.disconnect_cube("192.168.1.10"))
