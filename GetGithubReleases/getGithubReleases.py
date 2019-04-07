# This script will collect completed issues from current milestones in Github and generate release notes

# QUICK REFERENCES to Python resources
# https://pygithub.readthedocs.io/en/latest/introduction.html
# https://pygithub.readthedocs.io/en/latest/reference.html
# https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b

# REQUIREMENTS
# This script requires the PyGithub library in your python environment - https://pygithub.readthedocs.io/en/latest/index.html

# config.json includes this content (with your own access token)
#
# {
#   "ACCESS_KEY": "your-access-key"
# }

import json

def trymakedir(path):
    try:
        os.makedirs(path)
    except Exception as e:
        # print(e)
        if not os.path.exists(path):
            raise Exception('failed to create output directory: ' + path)

def githubrelease(githubapi, githubaccount, githubrepo, githubmilestone, githubfolder):
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
    releasenotes = ""
    releasenotes = releasenotes + "### RELEASE NOTES for milestone [" + githubmilestone + "](https://github.com/" + githubaccount + "/" + githubrepo + "/milestone/" + str(milestonenumber) + "?closed=1)"
    releasenotes = releasenotes + "** Enhancements: ** \n" + enhancementlist
    releasenotes = releasenotes + "** Bugs: ** \n" + bugslist
    targetdir = githubfolder + "\\Releases"
    trymakedir(targetdir)
    file = open(“targetdir\\” + githubmilestone + ".md", ”w”)
    file.write(releasenotes)
    file.close()


def githubReleaseCKTools(githubapi):
    print("========= CKTools")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\CKTools\\"
    githubrelease(githubapi, 'SkyrimLL', 'CKTools', 'CKTools 2019',githubfolder)


def githubReleaseSD(githubapi):
    print("========= Sanguine Debauchery")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SanguineDebauchery\\"
    githubrelease(githubapi, 'SkyrimLL', 'SDPlus', 'SD 2019',githubfolder)


def githubReleaseSLDialogues(githubapi):
    print("========= SL Dialogues")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SexLab_Dialogues\\"
    githubrelease(githubapi, 'SkyrimLL', 'SDPlus', 'SLD 2019',githubfolder)


if __name__ == '__main__':
    from github import Github

    with open('config.json', 'r') as f:
        config = json.load(f)

    g = Github(base_url="https://api.github.com", login_or_token=config['ACCESS_KEY'])

    # ===== CK Tools
    githubReleaseCKTools(g)

    # ===== Sanguine Debauchery +
    githubReleaseSD(g)

    # ===== SL Dialogues
    githubReleaseSLDialogues(g)