import argparse
import subprocess


class Handler:
    server_ports = [
        2000,
        2001,
        2002,
        2003
    ]

    @classmethod
    def handle(cls):
        """Interpret the first command line argument, and redirect."""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "action",
            choices=["start", "stop"],
            help="The action to take",
        )

        args = parser.parse_args()

        action = getattr(cls, args.action)
        action()

    @classmethod
    def start(cls):
        cls.server_processes = [cls.start_server(port) for port in cls.server_ports]

    @classmethod
    def stop(cls):
        for port in cls.server_ports:
            cls.kill_process_via_port(port)

    @classmethod
    def kill_process_via_port(cls, port):
        try:
            result = subprocess.run(
                ["lsof", "-ti", f":{port}"], stdout=subprocess.PIPE, text=True
            )
            pid = result.stdout.strip()
            if pid:
                subprocess.run(["kill", "-9", pid])
                print(f"Process using port {port} (PID {pid}) terminated.")
            else:
                print(f"No process found using port {port}.")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    @classmethod
    def start_server(cls, port):
        command = f"python server.py {port}"
        subprocess.Popen(command, shell=True)


if __name__ == "__main__":
    Handler.handle()
