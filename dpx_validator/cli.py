import sys

from dpx_validator.models import MSG, UndefinedMessage


def create_commandline_logs(dpx_file, valid, logs):

    for msg_type, msg in logs:
        print(f"File {dpx_file} : {msg}")

        if msg_type == MSG["info"]:
            print(f"File {dpx_file}: {msg}")

        elif msg_type == MSG["error"]:
            print(f"File {dpx_file}: {msg}", file=sys.stderr)

        else:
            raise UndefinedMessage(
                f"Undefined message type {msg_type}")

    if valid:
        print(f"File {dpx_file} is valid")
    else:
        print(f"File {dpx_file} is invalid")
