from Utils.cli import takeUserInput
from Services.github_service import *
import sys

pull_request_id = int(takeUserInput())
print("Thank you for entering your PR id")
# print("Your PR id is "+pull_request_id)

github_service = GithubService(pull_request_id)
val = github_service.get_latest_commit(pull_request_id)
print(val)

