# Class to serve all the request related to PR and sanity
class GithubService:
    def __init__(pr_number, branch):
        self.pr_number = pr_number

    def get_all_target(pr_number):
        # check whether the PR is valid or not, add try catch
        verify_pr_number(pr_number)
        # Use API

    def get_latest_commit(pr_number):
        # Use API

    def get_parent_commit(sha):
        # Use API

    def verify_pr_number(pr_number):    
        # Use API

    def get_pr_number(sha):
        # Use API    