# This script will collect completed issues from current milestones in Github and generate release notes

# QUICK REFERENCES to Python resources
# https://pygithub.readthedocs.io/en/latest/introduction.html
# https://pygithub.readthedocs.io/en/latest/reference.html
# https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b
# https://docs.github.com/rest

# To refresh token:
# https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

# REQUIREMENTS
# This script requires the PyGithub library in your python environment - https://pygithub.readthedocs.io/en/latest/index.html

# config.json includes this content (with your own access token)
#
# {
#   "ACCESS_KEY": "your-access-key"
# }

import json
import os
from github import Github
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


def try_makedir(path):
    try:
        os.makedirs(path)
    except Exception as e:
        # print(e)
        if not os.path.exists(path):
            raise Exception('failed to create output directory: ' + path)


def get_github_release(_github_api, _github_account, _github_repo, _github_milestone, _github_folder):
    repo = _github_api.get_repo(_github_account + '/' + _github_repo)
    closed_issues = repo.get_issues(state='closed')
    enhancement_list = ""
    bugs_list = ""
    milestone_number = 0
    for issue in closed_issues:
        milestone = issue.milestone
        # if milestone.title == 'SD 2019':
        if milestone is not None:
            if milestone.title == _github_milestone:
                milestone_number = milestone.number
                issue_number = issue.number
                for label in issue.labels:
                    issue_link = "- [" + issue.title + "](https://github.com/" + _github_account + "/" + _github_repo + "/issues/" + str(issue_number) + ")\n"
                    if label.name == 'enhancement':
                        enhancement_list = enhancement_list + issue_link
                    elif label.name == 'bug':
                        bugs_list = bugs_list + issue_link
    if milestone_number != 0:
        release_notes = ""
        release_notes = release_notes + "### RELEASE NOTES for milestone [" + _github_milestone + "](https://github.com/" + _github_account + "/" + _github_repo + "/milestone/" + str(milestone_number) + "?closed=1) \n"
        release_notes = release_notes + "**Enhancements:** \n" + enhancement_list + "\n"
        release_notes = release_notes + "**Bug Fixes:** \n" + bugs_list + "\n"

        target_folder = _github_folder + "Releases"
        target_file = target_folder + "\\" + _github_milestone + '.md'
        print("     Release notes: " + target_file)
        try_makedir(target_folder)
        file = open(target_file,'w')
        file.write(release_notes)
        file.close()
        print(target_file)


def process_release(_github_api, _github_account, _github_root_folder, _github_repo, _mod_path, _mod_name, _release_date):
    github_milestone = _mod_name + " " + _release_date
    github_folder = _github_root_folder + _github_repo + "\\"

    if (_mod_path != ''):
        github_folder = github_folder + _mod_path

    github_folder = github_folder + _mod_name + "\\"
 
    print(f"{Fore.BLUE}========= " + _mod_name + " " + _release_date + f"{Style.RESET_ALL}")
    print("     Local files: " + github_folder)
    print("     GitHub repo: " + _github_repo)

    get_github_release(_github_api, _github_account, _github_repo, github_milestone, github_folder)


if __name__ == '__main__':
    colorama_init()

    with open('config.json', 'r') as f:
        config = json.load(f)

    github_api = Github(base_url="https://api.github.com", login_or_token=config['ACCESS_KEY'])

    github_account = 'SkyrimLL'
    github_root_folder = "G:\\Games-data\\CustomMods\\_Github\\SkyrimLL\\"

    release_date = '2023-02-26'
 
    process_release(github_api, github_account, github_root_folder, 'CKTools', '', 'DeployCKFiles', release_date)
    process_release(github_api, github_account, github_root_folder, 'CKTools', '', 'GetGithubReleases', release_date)
    
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'LE\\', 'Parasites', release_date)
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'SE\\', 'Parasites', release_date)
    
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'LE\\', 'Hormones', release_date)
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'SE\\', 'Hormones', release_date)
    
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'LE\\', 'SisterhoodOfDibella', release_date)
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'SE\\', 'SisterhoodOfDibella', release_date)
    
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'LE\\', 'SexLabDialogues', release_date)
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'SE\\', 'SexLabDialogues', release_date)
    
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'LE\\', 'SanguineDebauchery', release_date)
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'SE\\', 'SanguineDebauchery', release_date)
    
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'LE\\', 'SkyrimImmersionPatch', release_date)
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'SE\\', 'SkyrimImmersionPatch', release_date)
    
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'LE\\', 'SexLabWarmBodies', release_date)
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'SE\\', 'SexLabWarmBodies', release_date)
    
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'LE\\', 'SexLabMindControl', release_date)
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'SE\\', 'SexLabMindControl', release_date)
    
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'LE\\', 'FamilyTies', release_date)
    process_release(github_api, github_account, github_root_folder, 'Skyrim', 'SE\\', 'FamilyTies', release_date)


