from Utils.cli import takeUserInput
from Utils.common import *
from Utils.jobd_helper import *
from pprint import pprint
from Services.github_service import *


def find_matching_master_build(github_service, commit_id, dic_of_master_builds, pr_id):
    pr_list = []
    while(True):
        pr_number = github_service.get_pr_number(commit_id)
        if pr_number is not None:
            pr_list.append(pr_number) 
        else:
            pr_list.append(pr_id) 
        if commit_id in dic_of_master_builds.keys():
            return pr_list, dic_of_master_builds[commit_id]
        commit_id = github_service.get_parent_commit(commit_id)
    return pr_to_sha

def get_all_pr_failed_root_jobs(pr_list, github_service):
    pr_to_root = []
    for val in pr_list:
        sha = github_service.get_latest_commit(val)
        failed_jobs = github_service.get_all_jobs(sha)
        root_job_id = get_root_job_id(failed_jobs)
        #print(val, failed_jobs)
        if root_job_id is not None:
            pr_root_target = get_target_info(root_job_id)
            pr_root_target = convert_target_dictionary(pr_root_target)
            dic = {}
            dic[val] = pr_root_target
            pr_to_root.append(dic)
    return pr_to_root

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
        pr_root_target = get_failed_root_jobs(root_job_id, True)
        pr_root_target = convert_target_dictionary(pr_root_target)
        print("Fetched failed target info:\n",end="")
        pprint(pr_root_target)
        dic_of_master_builds = get_master_builds()
        pr_list, matching_master_build = find_matching_master_build(github_service, sha, dic_of_master_builds, pull_request_id)
        pr_list.reverse()
        print(pr_list)
        master_root_target = get_all_jobs_and_targets_info(matching_master_build['ID'])
        master_root_target = convert_target_dictionary(master_root_target)
        print("Fetched target info from master build:\n ",end="")
        pprint(master_root_target)
        pr_to_root = get_all_pr_failed_root_jobs(pr_list, github_service)
        pprint(pr_to_root)
main()
