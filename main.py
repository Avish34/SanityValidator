from Utils.cli import takeUserInput
from Utils.common import *
from Utils.jobd_helper import *
from pprint import pprint
from Services.github_service import *
import sys

def main():
    pull_request_id = int(takeUserInput())
    print("Thank you for entering your PR id")

    github_service = GithubService(pull_request_id)
    sha = github_service.get_latest_commit(pull_request_id)
    pr_info = github_service.get_pr_info(pull_request_id)

    print(f"\nParent commit id {sha}\n")

    failed_jobs = github_service.get_failed_jobs(sha)
    pprint(f"Failed jobs are: {failed_jobs}")

    root_job_id = get_root_job_id(failed_jobs)
    print(f"\nFetched root job id: {root_job_id}\n")

    target_names = get_target_info(root_job_id)
    pprint(f"Fetched target info: {target_names}")

main()
