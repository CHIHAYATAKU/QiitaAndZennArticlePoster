# HandLingGit.py
import subprocess


def run_git_command(command, cwd=None):
    result = subprocess.run(
        command, cwd=cwd, shell=True, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise Exception(f"Error: {result.stderr}")
    return result.stdout


def git_switch_main(cwd=None):
    return run_git_command(f"git switch main", cwd)


def git_switch(branch="qiita", cwd=None):
    # ブランチが存在するかチェック
    branches = run_git_command("git branch --list", cwd).split()
    if branch not in branches:
        print(f"Error: Branch '{branch}' does not exist.")
        return False
    # git switch コマンドを実行
    return run_git_command(f"git switch {branch}", cwd)


def git_new_switch(branch="qiita", cwd=None):
    return run_git_command(f"git switch -c {branch}", cwd)


def git_add(files=".", cwd=None):
    return run_git_command(f"git add {files}", cwd)


def git_commit(message, cwd=None):
    return run_git_command(f'git commit -m "{message}"', cwd)


def git_push(remote="origin", branch="qiita", cwd=None):
    return run_git_command(f"git push -f {remote} {branch}", cwd)
