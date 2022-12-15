from pprint import pprint

import requests

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
    pprint(targets)
    target_names = list()

    for target in targets:
        if target["Success"] is True:
            target_names.append({"name": target["Name"], "status": "success"})
        else:
            target_names.append({"name": target["Name"], "status": "failure"})

    for i in range(len(target_names)):
        target_names[i]['name'] = target_names[i]['name'].replace('/','%2F')

    return target_names
