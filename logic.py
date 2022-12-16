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

def get_the_final_commit_internal(pr_target, pr_status, pr_to_root, pr_list):
    length = len(pr_list)
    final_result = 0
    for i in range(1,length-1):
        prid_with_targets_dict = pr_to_root[i]
        prid_targets = prid_with_targets_dict[pr_list[i]]
        if pr_target in prid_targets.keys():
            if prid_targets[pr_target] == 'success':
                final_result = 0
                continue
            else:
                if final_result == 0:
                    final_result = pr_list[i]
        else:
            continue
    if final_result == 0:
        return pr_target,pr_list[length-1]
    else:
        return pr_target,final_result

def get_the_final_commit(target,status,pr_to_root, pr_list, build_pr_target):
    
    if target not in build_pr_target.keys():
        return target,"Target not found on build"
    for build_target,build_status in build_pr_target.items():
        if target == build_target:
            if build_status == 'failure':
                return target,"Sanity validator needs build to have target status as success to go ahead"
            else:
                pr_target,final_result = get_the_final_commit_internal(target, status, pr_to_root, pr_list)
                return pr_target,final_result
    return 0,0

def get_the_root_target(pr_to_root, pr_list, build_pr_target, my_pr_target):
    length = len(pr_list)
    pr_id_for_that_target = []
    # pprint(build_pr_target)
    for target,status in my_pr_target.items():
        if status != 'success':
            pr_target,result = get_the_final_commit(target,status, pr_to_root,pr_list, build_pr_target)
            pr_id_for_that_target.append({pr_target:result})
    return pr_id_for_that_target


def get_failed_targets(pull_request_id):
    github_service = GithubService(pull_request_id)
    sha = github_service.get_latest_commit(pull_request_id)
    pr_info = github_service.get_pr_info(pull_request_id)

    failed_jobs = github_service.get_failed_jobs(sha)
    root_job_id = get_root_job_id(failed_jobs)

    if root_job_id is not None:
        pr_root_target = get_failed_root_jobs(root_job_id)
        pr_root_target = convert_target_dictionary(pr_root_target)
        dic_of_master_builds = get_master_builds()
        pr_list, matching_master_build = find_matching_master_build(github_service, sha, dic_of_master_builds, pull_request_id)
        pr_list.reverse()
        master_root_target = get_all_jobs_and_targets_info(matching_master_build['ID'])
        master_root_target = convert_target_dictionary(master_root_target)
        pr_to_root = get_all_pr_failed_root_jobs(pr_list, github_service)
        '''
        code for injecting failure
        # pprint(pr_to_root)
        # pr_to_root[10][60506]['build-apollo-x86-elba'] = 'failure'
        # pr_to_root[9][pr_list[9]]['build-apollo-x86-elba'] = 'failure'
        # pr_to_root[8][pr_list[8]]['build-apollo-x86-elba'] = 'failure' 
        '''
        final_result = get_the_root_target(pr_to_root, pr_list, master_root_target, pr_root_target)
        
        return final_result