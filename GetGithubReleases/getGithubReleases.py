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


def githubReleaseCKTools(githubapi, releasedate):
    print("========= CKTools")
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\CKTools\\"
    githubrelease(githubapi, 'SkyrimLL', 'CKTools', 'CKTools ' + releasedate, githubfolder)


def githubReleaseSD(githubapi, releasedate):
    print("========= Sanguine Debauchery")
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SanguineDebauchery\\"
    # githubrelease(githubapi, 'SkyrimLL', 'SDPlus', 'SD 2019',githubfolder)
    githubrelease(githubapi, 'SkyrimLL', 'SDPlus', 'SD ' + releasedate, githubfolder)


def githubReleaseSLD(githubapi, releasedate):
    print("========= SL Dialogues")
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SexLab_Dialogues\\"
    # githubrelease(githubapi, 'SkyrimLL', 'SDPlus', 'SLD 2019',githubfolder)
    githubrelease(githubapi, 'SkyrimLL', 'SDPlus', 'SLD ' + releasedate, githubfolder)


def githubReleaseSLSD(githubapi, releasedate):
    print("========= Sisterhood of Dibella")
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\SisterhoodOfDibella\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLmods', 'Sisterhood ' + releasedate, githubfolder)


def githubReleaseAlicia(githubapi, releasedate):
    print("========= Alicia")
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Alicia\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLmods', 'Alicia ' + releasedate, githubfolder)


def githubReleaseHormones(githubapi, releasedate):
    print("========= Hormones")
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Hormones\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLmods', 'Hormones ' + releasedate, githubfolder)


def githubReleaseParasites(githubapi, releasedate):
    print("========= Parasites")
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Parasites\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLmods', 'Parasites ' + releasedate, githubfolder)


def githubReleaseFamilyTies(githubapi, releasedate):
    print("========= Family Ties")
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\FamilyTies\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLmods', 'Family Ties ' + releasedate, githubfolder)

def githubReleaseStories(githubapi, releasedate):
    print("========= Stories")
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Stories\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLmods', 'Stories ' + releasedate, githubfolder)

def githubReleaseCollegeDaysPatch(githubapi, releasedate):
    print("========= Obscure Patches - College Days")
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\CollegeDaysPatch\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLpatches', 'College Days of Winterhold ' + releasedate, githubfolder)

def githubReleasePuppetMasterPatch(githubapi, releasedate):
    print("========= Obscure Patches - Puppet Master")
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\PuppetMasterPatch\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLpatches', 'Puppet Master ' + releasedate, githubfolder)

def githubReleaseSexLabWarmBodiesPatch(githubapi, releasedate):
    print("========= Obscure Patches - SexLab Warm Bodies")
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\SexLabWarmBodiesPatch\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLpatches', 'Warm Bodies ' + releasedate, githubfolder)

def githubReleaseLoversComfortPatch(githubapi, releasedate):
    print("========= Obscure Patches - Lovers Comfort Bodies")
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\LoversComfortPatch\\"
    githubrelease(githubapi, 'SkyrimLL', 'SkLLpatches', 'Lovers Comfort ' + releasedate, githubfolder)


if __name__ == '__main__':
    from github import Github

    with open('config.json', 'r') as f:
        config = json.load(f)

    g = Github(base_url="https://api.github.com", login_or_token=config['ACCESS_KEY'])

    # ===== CK Tools
    # githubReleaseCKTools(g)

    # ===== Sanguine Debauchery +
    githubReleaseSD(g, "2021-05-31")

    # ===== SL Dialogues
    # githubReleaseSLD(g, "2021-05-31")

    # ===== Sisterhood of Dibella
    # githubReleaseSLSD(g, "2021-02-28")

    # ===== Alicia
    # githubReleaseAlicia(g, "2021-05-31")

    # ===== Hormones
    githubReleaseHormones(g, "2021-05-31")

    # ===== Parasites
    githubReleaseParasites(g, "2021-05-31")

    # ===== Family Ties
    # githubReleaseFamilyTies(g, "2021-05-31")
    
    # ===== Stories
    githubReleaseStories(g, "2021-05-31")

    # ===== Obscure Patches
    # githubReleaseCollegeDaysPatch(g, "2021-05-31")
    # githubReleasePuppetMasterPatch(g, "2021-05-31")
    # githubReleaseSexLabWarmBodiesPatch(g, "2021-05-31")
    # githubReleaseLoversComfortPatch(g, "2021-05-31")

