from Utils.cli import takeUserInput
from Utils.common import *
from Utils.jobd_helper import *
from pprint import pprint
from Services.github_service import *


def find_matching_master_build(github_service, commit_id, dic_of_master_builds, pr_id):
    pr_to_sha = {}
    while(True):
        pr_number = github_service.get_pr_number(commit_id)
        if pr_number is not None:
            pr_to_sha[pr_number] = commit_id
        else:
            pr_to_sha[pr_id] = commit_id    
        if commit_id in dic_of_master_builds.keys():
            return pr_to_sha, dic_of_master_builds[commit_id]
        commit_id = github_service.get_parent_commit(commit_id)
    return pr_to_sha

def main():
    pull_request_id = int(takeUserInput())
    print("Thank you for entering your PR id")

    github_service = GithubService(pull_request_id)
    sha = github_service.get_latest_commit(pull_request_id)
    pr_info = github_service.get_pr_info(pull_request_id)

    print(f"\nParent commit id {sha}\n")

    failed_jobs = github_service.get_failed_jobs(sha)
    # pprint(f"Failed jobs are: {failed_jobs}")

    root_job_id = get_root_job_id(failed_jobs)
    # print(f"\nFetched root job id: {root_job_id}\n")

    if root_job_id is not None:
        pr_root_target = get_failed_root_jobs(root_job_id)
        pr_root_target = convert_target_dictionary(pr_root_target)
        print("Fetched failed target info:\n",end="")
        pprint(pr_root_target)
        dic_of_master_builds = get_master_builds()
        pr_to_sha, matching_master_build = find_matching_master_build(github_service, sha, dic_of_master_builds, pull_request_id)
        print(pr_to_sha)
        master_root_target = get_all_jobs_and_targets_info(matching_master_build['ID'])
        master_root_target = convert_target_dictionary(master_root_target)
        print("Fetched target info from master build:\n ",end="")
        pprint(master_root_target)
main()
