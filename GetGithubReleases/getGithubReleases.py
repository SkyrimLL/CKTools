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
import os

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
    milestonenumber = 0
    for issue in closed_issues:
        milestone = issue.milestone
        # if milestone.title == 'SD 2019':
        if milestone is not None:
            if milestone.title == githubmilestone:
                milestonenumber = milestone.number
                issuenumber = issue.number
                for label in issue.labels:
                    issuelink = "- [" + issue.title + "](https://github.com/" + githubaccount + "/" + githubrepo + "/issues/" + str(issuenumber) + ")\n"
                    if label.name == 'enhancement':
                        enhancementlist = enhancementlist + issuelink
                    elif label.name == 'bug':
                        bugslist = bugslist + issuelink
    if milestonenumber != 0:
        releasenotes = ""
        releasenotes = releasenotes + "### RELEASE NOTES for milestone [" + githubmilestone + "](https://github.com/" + githubaccount + "/" + githubrepo + "/milestone/" + str(milestonenumber) + "?closed=1) \n"
        releasenotes = releasenotes + "**Enhancements:** \n" + enhancementlist + "\n"
        releasenotes = releasenotes + "**Bug Fixes:** \n" + bugslist + "\n"

        targetfolder = githubfolder + "Releases"
        targetfile = targetfolder + "\\" + githubmilestone + '.md'
        trymakedir(targetfolder)
        file = open(targetfile,'w')
        file.write(releasenotes)
        file.close()
        print(targetfile)


def githubReleaseCKTools(githubapi):
    print("========= CKTools")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\CKTools\\"
    githubrelease(githubapi, 'SkyrimLL', 'CKTools', 'CKTools 2020', githubfolder)


def githubReleaseSD(githubapi):
    print("========= Sanguine Debauchery")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SanguineDebauchery\\"
    # githubrelease(githubapi, 'SkyrimLL', 'SDPlus', 'SD 2019',githubfolder)
    githubrelease(githubapi, 'SkyrimLL', 'SDPlus', 'SD 2020-06-30', githubfolder)


def githubReleaseSLD(githubapi):
    print("========= SL Dialogues")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SexLab_Dialogues\\"
    # githubrelease(githubapi, 'SkyrimLL', 'SDPlus', 'SLD 2019',githubfolder)
    githubrelease(githubapi, 'SkyrimLL', 'SDPlus', 'SLD 2020-06-30', githubfolder)


def githubReleaseSLSD(githubapi):
    print("========= Sisterhood of Dibella")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\SisterhoodOfDibella\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLmods', 'Sisterhood 2020-06-30', githubfolder)


def githubReleaseAlicia(githubapi):
    print("========= Alicia")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Alicia\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLmods', 'Alicia 2020-03-29', githubfolder)


def githubReleaseHormones(githubapi):
    print("========= Hormones")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Hormones\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLmods', 'Hormones 2020-07-25', githubfolder)


def githubReleaseParasites(githubapi):
    print("========= Parasites")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Parasites\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLmods', 'Parasites 2020-07-25', githubfolder)


def githubReleaseFamilyTies(githubapi):
    print("========= Family Ties")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\FamilyTies\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLmods', 'Family Ties 2020-06-30', githubfolder)

def githubReleaseStories(githubapi):
    print("========= Stories")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Stories\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLmods', 'Stories 2020-06-30', githubfolder)

def githubReleaseCollegeDaysPatch(githubapi):
    print("========= Obscure Patches - College Days")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\CollegeDaysPatch\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLpatches', 'College Days of Winterhold 2020-03-29', githubfolder)

def githubReleasePuppetMasterPatch(githubapi):
    print("========= Obscure Patches - Puppet Master")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\PuppetMasterPatch\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLpatches', 'Puppet Master 2020-03-29', githubfolder)

def githubReleaseSexLabWarmBodiesPatch(githubapi):
    print("========= Obscure Patches - SexLab Warm Bodies")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\SexLabWarmBodiesPatch\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLpatches', 'Warm Bodies 2020-07-25', githubfolder)

def githubReleaseLoversComfortPatch(githubapi):
    print("========= Obscure Patches - Lovers Comfort Bodies")
    githubfolder = "E:\\Games-data\\TESV-Skyrim\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\LoversComfortPatch\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLpatches', 'Lovers Comfort 2020-07-25', githubfolder)


if __name__ == '__main__':
    from github import Github

    with open('config.json', 'r') as f:
        config = json.load(f)

    g = Github(base_url="https://api.github.com", login_or_token=config['ACCESS_KEY'])

    # ===== CK Tools
    # githubReleaseCKTools(g)

    # ===== Sanguine Debauchery +
    # githubReleaseSD(g)

    # ===== SL Dialogues
    # githubReleaseSLD(g)

    # ===== Sisterhood of Dibella
    # githubReleaseSLSD(g)

    # ===== Alicia
    # githubReleaseAlicia(g)

    # ===== Hormones
    githubReleaseHormones(g)

    # ===== Parasites
    githubReleaseParasites(g)

    # ===== Family Ties
    # githubReleaseFamilyTies(g)
    
    # ===== Stories
    # githubReleaseStories(g)

    # ===== Obscure Patches
    # githubReleaseCollegeDaysPatch(g)
    # githubReleasePuppetMasterPatch(g)
    githubReleaseSexLabWarmBodiesPatch(g)
    githubReleaseLoversComfortPatch(g)

