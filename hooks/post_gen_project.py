#!/usr/bin/env python
import os
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    """Remove a file if it exists."""
    try:
        os.remove(os.path.join(PROJECT_DIRECTORY, filepath))
    except FileNotFoundError:
        pass


def execute(*args, suppress_exception=False, cwd=None):
    """Execute a command and return is stdout as a string."""
    proc = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd
    )

    out, err = proc.communicate()
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    if err and not suppress_exception:
        raise Exception(err)
    else:
        return out


def init_git():
    """Init git project if it's not initialized yet."""
    if not os.path.exists(os.path.join(PROJECT_DIRECTORY, ".git")):
        execute("git", "init", cwd=PROJECT_DIRECTORY)


def install_pre_commit_hooks():
    """Install a pre-commit hook."""
    execute("pre-commit", "install")


if __name__ == "__main__":

    if "{{ cookiecutter.create_author_file }}" != "y":
        remove_file("AUTHORS.md")
        remove_file("docs/authors.md")

    if "Not open source" == "{{ cookiecutter.open_source_license }}":
        remove_file("LICENSE")

    try:
        init_git()
    except Exception as e:
        print(e)

    if "{{ cookiecutter.install_precommit_hooks }}" == "y":
        install_pre_commit_hooks()
