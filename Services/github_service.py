import Utils.gh_helper as helper

# Class to serve all the request related to PR and sanity
class GithubService:
    def __init__(self, pr_number):
        self.pr_number = pr_number

    def get_all_target(self, pr_number):
        pass

    def get_latest_commit(self, pr_number):
        return helper.get_latest_commit(pr_number)

    def get_parent_commit(self, sha):
        pass

    def verify_pr_number(self, pr_number):
        pass

    def get_pr_number(self, sha):
        return helper.get_pr_num_from_sha(sha)

    def get_pr_info(self, pr_number):
        return helper.get_pr_info(pr_number)

    def get_failed_jobs(self, sha):
        return helper.get_failed_jobs(sha)

    def get_parent_commit(self, sha):
        return helper.get_parent_commit(sha)

    def get_all_jobs(self, sha):
        return helper.get_all_jobs(sha)    
