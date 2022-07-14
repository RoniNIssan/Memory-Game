import socket


class Protocol:

    def __init__(self):
        self.COMMANDS = {
            "WELCOME": b'WLCM',
            "WAIT": b'WAIT',
            "READY": b'REDY',
            "BOARD": b'BORD'
        }
        self.SEPARATOR = b'#'
        self.DECLARE_END = b'$'

    def get_welcome_command(self):
        return self.COMMANDS["WELCOME"]

    def get_wait_command(self):
        return self.COMMANDS["WAIT"]

    def get_ready_command(self):
        return self.COMMANDS["READY"]

    def get_board_command(self):
        return self.COMMANDS["BOARD"]

    def build_message(self, command: bytes, msg: bytes):
        return command + self.SEPARATOR + msg + self.DECLARE_END

    def send_message(self, message: bytes, sock: socket.socket):
        sock.send(message)

    def analyze_message(self, data: bytes):
        command = data[:4]

        if command == self.COMMANDS["WELCOME"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["WAIT"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["READY"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["BOARD"]:
            return data[5:]

    def separate_messages(self, data_bytes: bytes):
        print("data bytes")
        return data_bytes.split(self.DECLARE_END)
