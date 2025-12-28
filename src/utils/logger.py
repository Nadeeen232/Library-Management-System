from datetime import datetime


class Logger:
    def __init__(self, file_name="library.log"):
        self.file_name = file_name

    def log(self, message):
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.file_name, "a") as file:
            file.write(f"[{time_stamp}] {message}\n")
