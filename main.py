from Utils.cli import takeUserInput
from Utils.common import *
from Utils.jobd_helper import *
from pprint import pprint
from Services.github_service import *
from logic import *
from termcolor import colored

def main():
    pull_request_id = int(takeUserInput())
    print("Waiting for Status on PR...")
    failed_targets_pr = get_failed_targets(pull_request_id)
    if failed_targets_pr is not None:
        for val in failed_targets_pr:
            print(colored(list(val.keys())[0],'red'), ":", colored(list(val.values())[0], 'red'))
    else:
        print("Not handling for now.")

main()
