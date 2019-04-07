# This script will collect completed issues from current milestones in Github and generate release notes

# QUICK REFERENCES to Python resources
# https://pygithub.readthedocs.io/en/latest/introduction.html
# https://pygithub.readthedocs.io/en/latest/reference.html

# config.json includes this content (with your own access token)
#
# {
#   "ACCESS_KEY": "your-access-key"
# }

import json

def githubRelease(githubapi, githubaccount, githubrepo, githubmilestone):
    repo = githubapi.get_repo(githubaccount + '/' + githubrepo)
    closed_issues = repo.get_issues(state='closed')
    enhancementlist = ""
    bugslist = ""
    for issue in closed_issues:
        milestone = issue.milestone
        # if milestone.title == 'SD 2019':
        if milestone is not None:
            if milestone.title == githubmilestone:
                milestonenumber = milestone.number
                for label in issue.labels:
                    if label.name == 'enhancement':
                        enhancementlist = enhancementlist + "- " + issue.title + "\n"
                    elif label.name == 'bug':
                        bugslist = bugslist + "- " + issue.title + "\n"
    print ("### RELEASE NOTES for milestone [" + githubmilestone + "](https://github.com/" + githubaccount + "/" + githubrepo + "/milestone/" + str(milestonenumber) + "?closed=1)")
    print ("** Enhancements: ** \n" + enhancementlist)
    print ("** Bugs: ** \n" + bugslist)

def githubReleaseCKTools(githubapi):
    print("========= CKTools")
    githubRelease(githubapi, 'SkyrimLL', 'CKTools', 'CKTools 2019')

def githubReleaseSD(githubapi):
    print("========= Sanguine Debauchery")
    githubRelease(githubapi, 'SkyrimLL', 'SDPlus', 'SD 2019')

def githubReleaseSLDialogues(githubapi):
    print("========= SL Dialogues")
    githubRelease(githubapi, 'SkyrimLL', 'SDPlus', 'SLD 2019')


if __name__ == '__main__':
    from github import Github

    with open('config.json', 'r') as f:
        config = json.load(f)

    githubapi = Github(base_url="https://api.github.com", login_or_token=config['ACCESS_KEY'])

    # ===== CK Tools
    githubReleaseCKTools(githubapi)

    # ===== Sanguine Debauchery +
    githubReleaseSD(githubapi)

    # ===== SL Dialogues
    githubReleaseSLDialogues(githubapi)