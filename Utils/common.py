import re

def parse_job_id(description):
    job_id_regex = re.compile(r'#[0-9]+')
    match = job_id_regex.search(description)
    return match.group().split('#')[1]

def get_root_job_id(jobs):
    for job in jobs:
        if job['context'] == '*root*':
            return parse_job_id(job['description'])