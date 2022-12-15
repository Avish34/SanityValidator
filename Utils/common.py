import re

def parse_job_id(description):
    job_id_regex = re.compile(r'#[0-9]+')
    match = job_id_regex.search(description)
    return match.group().split('#')[1]

def get_root_job_id(jobs):
    for job in jobs:
        if job['context'] == '*root*':
            return parse_job_id(job['description'])

def parse_targets(target_name):
    res = target_name.split("%2F",1)
    return res[1]

def convert_target_dictionary(target_list):
    res_target_dict = {}
    for target_dictionary in target_list:
        target_dictionary['name'] = parse_targets(target_dictionary['name'])
        res_target_dict[target_dictionary['name']] = target_dictionary['status']
    return res_target_dict