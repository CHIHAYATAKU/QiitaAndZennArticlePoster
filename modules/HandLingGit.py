# HandLingGit.py
import subprocess


def run_git_command(command, cwd=None):
    result = subprocess.run(
        command, cwd=cwd, shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise Exception(f"Error: {result.stderr}")
    return result.stdout


def git_add(files=".", cwd=None):
    return run_git_command(f"git add {files}", cwd)


def git_commit(message, cwd=None):
    return run_git_command(f'git commit -m "{message}"', cwd)


def git_push(remote="origin", branch="main", cwd=None):
    return run_git_command(f"git push -f {remote} {branch}", cwd)
