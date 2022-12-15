from pprint import pprint
from github import Github
from functools import lru_cache

import os

ENV_GITHUB_TOKEN = "GITHUB_TOKEN"

@lru_cache(maxsize=1)
def get_github_object():
    """Retrieves the github.Github object.
    Expects the Github token in the OS environment variable defined in ENV_GITHUB_TOKEN
    Returns:
        github.Github: Github object
    """
    token = os.environ.get(ENV_GITHUB_TOKEN, None)
    if token is None:
        print("GITHUB TOKEN not found")
        raise ValueError(f"Github API token is expected in the environment variable {ENV_GITHUB_TOKEN}")
    return Github(token)


@lru_cache(maxsize=1)
def get_repo_object(owner_name, repo_name):
    """Retrieves the github.repository object for the given repo
    Args:
        owner_name (str): Name of the owner/org
        repo_name (str): Name of the Git repo within owner/org namespace
    """
    return get_github_object().get_repo(f"{owner_name}/{repo_name}")

def get_latest_commit(pr_num):
    """Method to get the latest commit of the pr

    Args:
        pr_num (int): Pr number
    """
    repo_obj = get_repo_object("pensando", "sw")
    pr = repo_obj.get_pull(pr_num)
    return pr.head.sha
