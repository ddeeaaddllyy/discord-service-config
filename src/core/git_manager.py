from src.utils.shell import run_command

class GitManager:

    def __init__(self, path):
        self.path = path

    def is_repo(self):
        out, _ = run_command("git rev-parse --is-inside-work-tree", self.path)
        return out == "true"

    def status(self):
        out, _ = run_command("git status --porcelain", self.path)
        return out.splitlines()

    def add_all(self):
        run_command("git add .", self.path)

    def commit(self, message):
        run_command(f'git commit -m "{message}"', self.path)

    def push(self):
        run_command("git push", self.path)