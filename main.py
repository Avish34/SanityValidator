from Utils.cli import takeUserInput
from Utils.common import *
from Utils.jobd_helper import *
from pprint import pprint
from Services.github_service import *


def find_matching_master_build(github_service, commit_id, dic_of_master_builds):
    while(True):
        if commit_id in dic_of_master_builds.keys():
            return dic_of_master_builds[commit_id]
        commit_id = github_service.get_parent_commit(commit_id)
    return


def main():
    pull_request_id = int(takeUserInput())
    print("Thank you for entering your PR id")

    github_service = GithubService(pull_request_id)
    sha = github_service.get_latest_commit(pull_request_id)
    pr_info = github_service.get_pr_info(pull_request_id)

    print(f"\nParent commit id {sha}\n")

    failed_jobs = github_service.get_failed_jobs(sha)
    #pprint(f"Failed jobs are: {failed_jobs}")

    root_job_id = get_root_job_id(failed_jobs)
    #print(f"\nFetched root job id: {root_job_id}\n")

    if root_job_id is not None:
        target_names = get_target_info(root_job_id)
        #pprint(f"Fetched target info: {target_names}")

        dic_of_master_builds = get_master_builds()
        #matching_master_build = find_matching_master_build(github_service, sha, dic_of_master_builds)
        ### Testing code ###
        matching_master_build = dic_of_master_builds['74f9ccf2cede4c8dab081a54c980c6936aaa1aea']
        print(matching_master_build['ID'])
        master_root_target = get_all_jobs_and_targets_info(matching_master_build['ID'])
        pprint(master_root_target)

main()
