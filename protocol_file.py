import socket
import pickle
import elements


class Protocol:

    def __init__(self):
        self.COMMANDS = {
            "WELCOME": b'WLCM',
            "CATEGORY": b'CTGY',
            "WAIT": b'WAIT',
            "READY": b'REDY',
            "BOARD": b'BORD',
            "MY TURN": b'MTRN',
            "OTHER TURN": b'OTRN',
            "CORRECT": b'CRCT',
            "WRONG": b'WRNG',
            "WIN": b'WING',
            "LOOSE": b'LOST',
            "TIE": b'TIEG',
            "END": b'ENDG'
        }
        self.SEPARATOR = b'#'
        self.DECLARE_END = b'$'

    def get_welcome_command(self):
        return self.COMMANDS["WELCOME"]

    def get_category_command(self):
        return self.COMMANDS["CATEGORY"]

    def get_wait_command(self):
        return self.COMMANDS["WAIT"]

    def get_ready_command(self):
        return self.COMMANDS["READY"]

    def get_board_command(self):
        return self.COMMANDS["BOARD"]

    def get_my_turn_command(self):
        return self.COMMANDS["MY TURN"]

    def get_other_turn_command(self):
        return self.COMMANDS["OTHER TURN"]

    def get_correct_command(self):
        return self.COMMANDS["CORRECT"]

    def get_wrong_command(self):
        return self.COMMANDS["WRONG"]

    def get_win_command(self):
        return self.COMMANDS["WIN"]

    def get_loose_command(self):
        return self.COMMANDS["LOOSE"]

    def get_tie_command(self):
        return self.COMMANDS["TIE"]

    def get_end_command(self):
        return self.COMMANDS["END"]

    def build_message(self, command: bytes, msg: bytes):
        return command + self.SEPARATOR + msg + self.DECLARE_END

    def send_message(self, message: bytes, sock: socket.socket):
        sock.send(message)

    def analyze_message(self, data: bytes):
        command = data[:4]

        if command == self.COMMANDS["WELCOME"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["CATEGORY"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["WAIT"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["READY"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["BOARD"]:
            return data[5:]

        if command == self.COMMANDS["MY TURN"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["OTHER TURN"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["CORRECT"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["WRONG"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["WIN"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["LOOSE"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["TIE"]:
            return data[5:].decode('UTF-8')

        if command == self.COMMANDS["END"]:
            return data[5:].decode('UTF-8')

    def separate_messages(self, data_bytes: bytes):
        return data_bytes.split(self.DECLARE_END)


def pack(obj: elements.Board) -> bytes:
    return pickle.dumps(obj)


def unpack(obj):
    return pickle.loads(obj)
