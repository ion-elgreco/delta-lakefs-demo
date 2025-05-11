import re
import subprocess

import dagster as dg


def get_git_branch() -> str:
    branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
    ).decode()

    branch = re.sub(r"[^a-zA-Z0-9]+", "-", branch).strip("-")  # Strips double --
    return branch


class CodeBranch(dg.ConfigurableResource):
    name: str
