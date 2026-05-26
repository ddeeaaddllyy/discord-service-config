import os
from src.core.git_manager import GitManager

def find_git_projects(base_paths):
    projects = []

    for base in base_paths:
        for root, dirs, files in os.walk(base):
            if ".git" in dirs:
                gm = GitManager(root)
                projects.append({
                    "path": root,
                    "git": gm
                })
                dirs[:] = []  # stop deeper scanning

    return projects