from pprint import pprint

import requests

master_build_url = "http://jobd.test.pensando.io:3456/submission?release=1&repo=pensando%2Fsw&branch=master&page=0&limit=50"

def get_target_info(job_id):
    """Method to get the target names of the particular job id

    Args:
        job_id (int): Job ID

    Returns:
        list: Contains target name with %2F
    """
    url = f"http://jobd.test.pensando.io:3456/job/{job_id}"
    res = requests.get(url)

    json_res = res.json()
    targets = json_res["Targets"]
   #pprint(targets)
    target_names = list()

    for target in targets:
        if target["Success"] is True:
            target_names.append({"name": target["Name"], "status": "success"})
        else:
            target_names.append({"name": target["Name"], "status": "failure"})

    for i in range(len(target_names)):
        target_names[i]['name'] = target_names[i]['name'].replace('/','%2F')

    return target_names

def get_master_builds():
    res = requests.get(master_build_url)
    master_builds = res.json()
    #pprint(json_res)
    dic_of_master_builds = {}
    for build in master_builds:
        sha = build['Jobs'][0]['Ref']['SHA']
        dic_of_master_builds[sha] = build
    
    return dic_of_master_builds

def get_all_jobs_and_targets_info(job_id):
    master_all_jobs_all_targets_url = f"http://jobd.test.pensando.io:3456/submission/{job_id}"
    res = requests.get(master_all_jobs_all_targets_url)
    # print(master_all_jobs_all_targets_url)
    json_res_all_targets = res.json()
    for job in json_res_all_targets['Jobs']:
        if job['SubPath'] == '':
            return get_target_info(job['ID'])
    return