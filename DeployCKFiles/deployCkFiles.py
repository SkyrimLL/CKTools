# This script will copy files from a source directory (skyrim/Data folder) to two target directories: one for backups and preparing BSA files and one for source control (github)

# Code adapted from: https://gist.github.com/Sleepingwell/6070119

# QUICK REFERENCES to Python resources
# https://docs.python.org/2/library/shutil.html
# https://www.pythonforbeginners.com/os/python-the-shutil-module
# http://xahlee.info/python/python_path_manipulation.html

""" 
Check the sample mods_manifest_sample.json file.
Rename to mods_manifest.json before use.
- All paths should end with a separator ( Remember to escape \\ on Windows. )

"""

import re
import os
import os.path
import shutil
import fnmatch
import filecmp
import json

debug = False

def deployModGroup(mods_data, mod_group_name):
    deployMods(mods_data, mod_group_name,"all")


def deployMod(mods_data, mod_group_name, mod_name):
    deployMods(mods_data, mod_group_name, mod_name)


def deployAllMods(mods_data):
    deployMods(mods_data, "all","all")


def deployMods(mods_data, mod_group_name, mod_name):
    mod_group_list = mods_data["mod_groups"]
    mod_group_match = 0
    mod_match = 0

    for this_mod_group in mod_group_list:  
        # print(this_mod_group)

        if (mod_group_name=="all") or (mod_group_name==this_mod_group['name']):
            mod_group_match += 1

            for this_mod in this_mod_group['mods']:  
                # print(this_mod)

                if (mod_name=="all") or (mod_name==this_mod['name']):
                    mod_match += 1

                    print("========= " + this_mod_group['name'] + " - " + this_mod['name'])
                    source_folder = this_mod["source_folder"]
                    release_folder = this_mod["release_folder"]
                    github_folder = this_mod["github_folder"]
                    mod_assets = this_mod["assets"] 
                    mode = this_mod["mode"]

                    # print(source_folder)
                    # print(release_folder)
                    # print(github_folder)
                    # print(mod_assets)
                    # print(mode)

                    deployfiles([source_folder], [release_folder, github_folder], mod_assets, mode)

    if (mod_group_match == 0):
            print(":: No mod group deployed")

    if (mod_match == 0):
            print(":: No mods deployed")


def deployfiles(source_list, destination_list, modassets_list, mode):
    for asset in modassets_list:
        filepattern_list = asset["file_patterns"]

        for source in source_list:
            for destination in destination_list:
                for filepattern in filepattern_list:
                    if not (destination==""):
                        if not debug:
                            trymakedir(destination)

                    if (not os.path.exists(source + asset["path"])):
                        print(">> Invalid Source folder: " + source + asset["path"])
                    else:
                        if not (destination==""):
                            if not debug:
                                docopy(source + asset["path"], destination + asset["path"], filepattern)
                            else:
                                print("> Source: " + source + asset["path"])
                                print("> Target: " + destination + asset["path"])
                                print("> Pattern: " + filepattern)


def docopy(inputdir, outputdir, pattern):
    foundfiles = ""
    regexpattern = fnmatch.translate(pattern)
    prog = re.compile(regexpattern)

    totalfilecount = 0
    for (root, dirs, files) in os.walk(inputdir):
        filecount = 0
        for fn in files:
            m = prog.match(fn)
            if m:
                targetdir = join(outputdir, os.path.relpath(root, inputdir))
                if not debug:
                    trymakedir(targetdir)
                
                # Exclude some files
                if (fn != "Thumbs.db") and (not (".vortex_backup" in fn)):
                    # If file is newer, or if filesize is different in case os .esp (because of load order)
                    copyfileflag = False
                    if (not os.path.exists(join(targetdir, fn))):
                        foundfiles = foundfiles + "\n" + "Found new file " + join(targetdir, fn)
                        copyfileflag = True
                    elif (os.path.exists(join(root, fn)) and os.path.exists(join(targetdir, fn))):
                        if (os.path.getmtime(join(root, fn)) > os.path.getmtime(join(targetdir, fn))):
                            # Copy newer files - updated recently
                            foundfiles = foundfiles + "\n" + "Updating newer file " + join(targetdir, fn)
                            copyfileflag = True
                        elif (not filecmp.cmp(join(root, fn), join(targetdir, fn))):
                            # Copy new or missing files
                            foundfiles = foundfiles + "\n" + "Updating different file " + join(targetdir, fn)
                            copyfileflag = True
                        # elif (".esp" in fn) or (".esm" in fn):
                           # Force copy of esp and esm files (because of timestamps used for load order)
                           # foundfiles = foundfiles + "\n" + "Updating file " + join(targetdir, fn)
                           # copyfileflag = True

                    if (copyfileflag):
                        if not debug:
                            shutil.copy(join(root, fn), join(targetdir, fn))

                        # Disabled for issues with time
                        # if (".esp" in fn) or (".esm" in fn):
                        #    os.utime(join(targetdir, fn), None)
                        filecount = filecount + 1
        totalfilecount = totalfilecount + filecount
        if filecount != 0:
            print("----")
            print("Processing... " + pattern + " To: " + outputdir + foundfiles)
            print("     " + str(filecount) + " files in " + root)


def join(*args):
    return os.path.normpath(os.path.join(*args))


def trymakedir(path):
    try:
        os.makedirs(path)
    except Exception as e:
        # print(e)
        if not os.path.exists(path):
            raise Exception('>>> Failed to create output directory: ' + path)


def deploySD():
    print("========= Sanguine Debauchery")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Sanguine-Debauchery-Plus\\Dev\\SDPlus\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SanguineDebauchery\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['_sd*.*', '_SD*.*']
    modassets["SEQ\\"] = ['sanguinesDebauchery.SEQ']
    modassets["Interface\\_SD_\\"] = ['sanguine_rose.*']
    modassets["Interface\\Translations\\"] = ['sanguinesDebauchery*.*']
    modassets["meshes\\_sd_\\"] = ['_sd*.*', '*.*']
    modassets["meshes\\actors\\character\\animations\\sanguinesDebauchery\\"] = ['*.*']
    modassets["meshes\\actors\\character\\animations\\"] = ['idlehandsbehindback.hkx']
    modassets["meshes\\actors\\character\\behaviors\\"] = ['FNIS_sanguinesDebauchery_Behavior.hkx']
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\sanguinesDebauchery.esp\\"] = ['*.*']
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\Skyrim.esm\\"] = ['0003DC4A.NIF', '0003DC4E.NIF', '0003DC50.NIF','0003DC52.NIF']
    modassets[""] = ['sanguinesDebauchery.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("==== SD+ Resources")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Sanguine-Debauchery-Plus\\Dev\\SDResources\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SanguineDebauchery\\Data\\"

    modassets = {}

    modassets["textures\\_sd_\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\sanguinesDebauchery.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\Skyrim.esm\\"] = ['0003DC4A.*', '0003DC4E.*', '0003DC50.*', '0003DC52.*']
    modassets["textures\\actors\\character\\slavetats\\sdplus\\"] = ['*.*']
    modassets["textures\\actors\\character\\slavetats\\"] = ['sdplus.json']
    modassets["textures\\azmoscreens\\"] = ['*.*']
    modassets["textures\\bondage\\"] = ['*.*']
    modassets["textures\\sextoys-calyps\\"] = ['*.*']
    modassets["textures\\Sheogorad\\daedric\\"] = ['*.*']
    modassets["textures\\ZaZ\\Gagz\\"] = ['*.*']
    modassets["textures\\ZaZ\\Restraints\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("==== Revealing Male Spriggan")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Sanguine-Debauchery-Plus\\Dev\\RevealingMaleSpriggan\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\RevealingMaleSpriggan\\Data\\"

    modassets = {}
    modassets["meshes\\_sd_\\sprigganarmor\\male"] = ['SprigganCuirass_*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("==== SD Addon")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Sanguine-Debauchery-Plus\\Dev\\SD Addon\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SD Addon\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['sd_addon_*.*']
    modassets["SEQ\\"] = ['SD Addons.seq']
    modassets["Interface\\coco\\"] = ['sdaddon.*']
    modassets[""] = ['SD Addons.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("==== SlaveTat Event Bridge")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Sanguine-Debauchery-Plus\\Dev\\SlaveTatsEventsBridge\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SlaveTatsEventsBridge\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SlaveTatsEventsBridge*.*']
    modassets[""] = ['SlaveTatsEventsBridge.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deploySDVoicePack():
    print("========= Sanguine Debauchery Voice Pack")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Sanguine-Debauchery-Plus\\Dev\\SDVoicePack\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SanguineDebauchery\\Data\\"

    modassets = {}

    modassets["sound\\Voice\\sanguinesDebauchery.esp\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deploySLD():
    print("========= SL Dialogues")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-Dialogues\\Dev\\BSA\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SexLab_Dialogues\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SLD_*.*', 'SLD_*.*']
    modassets["meshes\\actors\\character\\SL_Dialogues\\"] = ['*.*']
    modassets["meshes\\clutter\\SL_Dialogues\\"] = ['*.*']
    modassets["textures\\clutter\\SL_Dialogues\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-Dialogues\\Dev\\Loose\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SDPlus\\SexLab_Dialogues\\Data\\"

    modassets = {}
    modassets["SEQ\\"] = ['SexLab_Dialogues.seq']
    modassets["Interface\\SexLab_Dialogues\\"] = ['*.*']
    modassets[""] = ['SexLab_Dialogues.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deploySLSD():
    print("========= Sisterhood of Dibella")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Dibella-Sisterhood\\Dev\\BSA\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\SisterhoodOfDibella\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SL_Dibella_*.*']
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\SexLab_DibellaCult.esp\\"] = ['*.*']
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\Skyrim.esm\\"] = ['0001E82C.NIF', '0001E765.NIF', '000133A5.NIF', '000133B0.NIF', '000133B7.NIF', '0001335F.NIF', '00013386.NIF']
    modassets["meshes\\armor\\SL_Dibella\\"] = ['*.*']
    modassets["meshes\\clutter\\SL_Dibella\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\SexLab_DibellaCult.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\Skyrim.esm\\"] = ['0001E82C.*', '0001E765.*', '000133A5.*', '000133B0.*', '000133B7.*', '0001335F.*', '00013386.*']
    modassets["textures\\armor\\SL_Dibella\\"] = ['*.*']
    modassets["textures\\clutter\\SL_Dibella\\"] = ['*.*']
    modassets["textures\\ashara\\Dimonized dress\\Skirt\\"] = ['*.*']
    modassets["textures\\azmoscreens\\"] = ['mrs3_gold*', 'ss*.*']
    modassets["textures\\azmoscreens\\statues\\"] = ['*.*']
    modassets["textures\\cubemaps\\"] = ['chitin_e_ebony.dds', 'quickskydark_eGD.dds']
    modassets["textures\\kasprutz\\armor\\bdo_kibelius\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Dibella-Sisterhood\\Dev\\Loose\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\SisterhoodOfDibella\\Data\\"

    modassets = {}
    modassets["SEQ\\"] = ['SexLab_DibellaCult.seq']
    modassets[""] = ['SexLab_DibellaCult.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    # ----
    print("========= Sisterhood of Dibella - Sisters addon")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Dibella-Sisterhood-Sisters\\Dev\\BSA\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\SisterhoodOfDibella\\Data\\"

    modassets = {}
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\SexLab_DibellaCult_Sisters.esp\\"] = ['*.*']
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\Skyrim.esm\\"] = ['0001E82C.NIF', '0001E765.NIF', '000133A5.NIF', '000133B0.NIF', '000133B7.NIF', '0001335F.NIF', '00013386.NIF']
    modassets["meshes\\armor\\SL_Dibella_Sisters\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\SexLab_DibellaCult_Sisters.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\Skyrim.esm\\"] = ['0001E82C.*', '0001E765.*', '000133A5.*', '000133B0.*', '000133B7.*', '0001335F.*', '00013386.*']
    modassets["textures\\armor\\SL_Dibella_Sisters\\"] = ['*.*']
    modassets["textures\\armor\\SL_Dibella\\"] = ['dibella_sister_outfit.dds','femalebody_1_s.dds','lilly.dds','lilly_n.dds','travel_hood.dds']
    modassets["textures\\armor\\Gatti\\"] = ['*.*']
    modassets["textures\\Ashara\\Imperial Wedding outfit\\"] = ['*.*']
    modassets["textures\\fox011\\f046\\"] = ['*.*']
    modassets["textures\\SexyLingerieSet\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Dibella-Sisterhood-Sisters\\Dev\\Loose\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\SisterhoodOfDibella\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SL_DibellaSisters*.*']
    modassets["SEQ\\"] = ['SexLab_DibellaCult_Sisters.seq']
    modassets[""] = ['SexLab_DibellaCult_Sisters.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployAlicia():
    print("========= Alicia")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Alicia-PainSlut\\Dev\\BSA\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Alicia\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['Alicia_*.*']

    modassets["sound\\Voice\\AliciaPainSlut.esp\\_Alicia_VOICE\\"] = ['*.*']

    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\AliciaPainSlut.esp\\"] = ['*.*']
    modassets["meshes\\actors\\character\\AliciaPainSlut\\"] = ['*.*']
    modassets["meshes\\armor\\AliciaPainSlut\\"] = ['*.*']
    modassets["meshes\\armor\\AliciaSanguineFollowers\\"] = ['*.*']
    modassets["meshes\\clutter\\AliciaPainSlut\\"] = ['*.*']
    modassets["meshes\\weapons\\AliciaPainSlut\\"] = ['*.*']

    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\AliciaPainSlut.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\AliciaPainSlut\\"] = ['*.*']
    modassets["textures\\_sd_\\shrine\\"] = ['*.*']
    modassets["textures\\armor\\AliciaPainSlut\\"] = ['*.*']
    modassets["textures\\azmoscreens\\"] = ['mrs3_gold*', 'ss*.*']
    modassets["textures\\azmoscreens\\statues\\"] = ['*.*']
    modassets["textures\\baronb\\dragon\\"] = ['*.*']
    modassets["textures\\clutter\\AliciaPainSlut\\"] = ['*.*']
    modassets["textures\\weapons\\AliciaPainSlut\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Alicia-PainSlut\\Dev\\Loose\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Alicia\\Data\\"

    modassets = {}
    modassets["SEQ\\"] = ['AliciaPainSlut.seq']
    modassets[""] = ['AliciaPainSlut.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployHormones():
    print("========= Hormones")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-Hormones\\Dev\\BSA\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Hormones\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SLH_*.*']

    modassets["sound\\FX\\SL_Hormones\\"] = ['bimbo*.*']

    modassets["meshes\\actors\\character\\animations\ZazAnimationPack\\"] = ['ZaZHorny*.*']
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\SexLab_Hormones.esp\\"] = ['*.*']
    modassets["meshes\\actors\\character\\SL_Hormones\\"] = ['*.*']
    modassets["meshes\\armor\\SL_Hormones\\"] = ['*.*']
    modassets["meshes\\clutter\\SL_Hormones\\"] = ['*.*']

    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\SexLab_Hormones.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\Rosa\\"] = ['*.*']
    modassets["textures\\actors\\character\\SL_Hormones\\"] = ['*.*']
    modassets["textures\\armor\\SL_Hormones\\"] = ['*.*']
    modassets["textures\\clutter\\SL_Hormones\\"] = ['*.*']
    modassets["textures\\_SLH\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-Hormones\\Dev\\Loose\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Hormones\\Data\\"

    modassets = {}
    modassets["Interface\\SexLab_Hormones\\"] = ['logo.dds']
    modassets["Interface\\Translations\\"] = ['SexLab_Hormones*.*']
    modassets["SEQ\\"] = ['SexLab_Hormones.seq']
    modassets["textures\\actors\\character\\slavetats\\bimbo\\"] = ['*.*']
    modassets["textures\\actors\\character\\slavetats\\"] = ['bimbo.json']
    modassets["textures\\actors\\character\\slavetats\\hormones\\"] = ['*.*']
    modassets["textures\\actors\\character\\slavetats\\"] = ['hormones.json']
    modassets["SKSE\\Plugins\\StorageUtilData\\SLHormones\\"] = ['*.*']
    modassets[""] = ['SexLab_Hormones.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployHormonesVoicePack():
    print("========= Hormones Voice Pack")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-Hormones\\Dev\\HormonesVoicePack\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Hormones\\Data\\"

    modassets = {}

    modassets["sound\\Voice\\SexLab_Hormones.esp\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployParasites():
    print("========= Parasites")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Kyne-Blessing\\Dev\\BSA\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Parasites\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SLP_*.*']

    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\SexLab-Parasites.esp\\"] = ['*.*']
    modassets["meshes\\armor\\KyneBlessing\\"] = ['*.*']
    modassets["meshes\\weapons\\KyneBlessing\\"] = ['*.*']
    modassets["meshes\\clutter\\KyneBlessing\\"] = ['*.*']
    modassets["meshes\\ZaZ-UltimateDataPack\\ZaZ - Furniture\\FuroTubReused\\"] = ['AoZaZFuroTents1.nif']

    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\SexLab-Parasites.esp\\"] = ['*.*']
    modassets["textures\\armor\\KyneBlessing\\"] = ['*.*']
    modassets["textures\\clutter\\KyneBlessing\\"] = ['*.*']

    modassets["textures\\TeraArmors\\castanic_f_r16\\"] = ['*.*']
    modassets["textures\\TeraArmors\\xTeraglassrobe\\"] = ['*.*']
    modassets["textures\\TeraArmors\\xteraelegance\\"] = ['*.*']
    modassets["textures\\TeraArmors\\zzterah21\\"] = ['*.*']
    modassets["textures\\teraarmors2\\Neophyte\\"] = ['*.*']
    modassets["textures\\TeraArmors2\\ZZCastanicL00\\"] = ['*.*']

    modassets["textures\\TeraArmorsM\\castanic_f_r16\\"] = ['*.*']
    modassets["textures\\TeraArmorsM\\xTeraglassrobe\\"] = ['*.*']
    modassets["textures\\TeraArmorsM\\xteraelegance\\"] = ['*.*']
    modassets["textures\\TeraArmorsM\\zzterah21\\"] = ['*.*']
    modassets["textures\\TeraArmorsM2\\Neophyte\\"] = ['*.*']
    modassets["textures\\TeraArmorsM2\\ZZCastanicL00\\"] = ['*.*']

    modassets["textures\\zaz\\xxfurotrap\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Kyne-Blessing\\Dev\\Loose\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Parasites\\Data\\"

    modassets = {}
    modassets["Interface\\KyneBlessing\\"] = ['logo.dds']
    modassets["SEQ\\"] = ['SexLab-Parasites.seq']
    modassets[""] = ['SexLab-Parasites.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployParasitesVoicePack():
    print("========= Parasites Voice Pack")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Kyne-Blessing\\Dev\\ParasitesVoicePack\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Parasites\\Data\\"

    modassets = {}

    modassets["sound\\Voice\\SexLab-Parasites.esp\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployMindControl():
    print("========= Mind Control")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-MindControl\\Dev\\BSA\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\MindControl\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SL_Hypnosis_*.*']

    modassets["meshes\\armor\\MindControlCirclet\\circlets\\"] = ['*.*']

    modassets["textures\\armor\\MindControlCirclet\\circlet\\"] = ['*.*']
    modassets["textures\\_SLMC\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-MindControl\\Dev\\Loose\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\MindControl\\Data\\"

    modassets = {}
    modassets["Interface\\SexLab_MindControl\\"] = ['logo.dds']
    modassets["SEQ\\"] = ['SexLab_MindControl.seq']
    modassets[""] = ['SexLab_MindControl.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployFamilyTies():
    print("========= Family Ties")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Family-Ties\\Dev\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\FamilyTies\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['FT_*.*']
    modassets["meshes\\actors\\character\\FamilyTies\\"] = ['*.*']
    modassets["textures\\actors\\character\\FamilyTies\\"] = ['*.*']
    modassets[""] = ['FamilyTies.esp', 'FamilyTies-*.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployStories():
    print("========= Stories")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-Stories\\Dev\\BSA\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Stories\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SLS_*.*']

    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\SexLab-Stories.esp\\"] = ['*.*']
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\Skyrim.esm\\"] = ['00013B9B.NIF', '000136BC.NIF', '000B1CFF.NIF', '0004815F.NIF']
    modassets["meshes\\actors\\character\\SL_Stories\\"] = ['*.*']
    modassets["meshes\\armor\\SL_Stories\\"] = ['*.*']
    modassets["meshes\\clutter\\SL_Stories\\"] = ['*.*']

    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\SexLab-Stories.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\Skyrim.esm\\"] = ['00013B9B.*', '000136BC.*', '000B1CFF.*', '0004815F.*']
    modassets["textures\\actors\\character\\SL_Stories\\"] = ['*.*']
    modassets["textures\\armor\\SL_Stories\\"] = ['*.*']
    modassets["textures\\clutter\\SL_Stories\\"] = ['*.*']
    modassets["Textures\\Dwarven Cyborg Collection\\gilded\\"] = ['*.*']
    modassets["textures\\azmoscreens\\pinups\\"] = ['*.*']
    modassets["textures\\Oaristys\\The Witcher\\Alchemy\\"] = ['*.*']
    modassets["textures\\Oaristys\\The Witcher\\Tools\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-Stories\\Dev\\Loose\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Stories\\Data\\"

    modassets = {}
    modassets["Interface\\SexLab_Stories\\"] = ['logo.dds']
    modassets["SEQ\\"] = ['SexLab-Stories.seq']
    modassets[""] = ['SexLab-Stories.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployStoriesVoicePack():
    print("========= Stories Voice Pack")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-Stories\\Dev\\StoriesVoicePack\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Stories\\Data\\"

    modassets = {}

    modassets["sound\\Voice\\SexLab-Stories.esp\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)



def deployStoriesDevious():
    print("========= Stories Devious")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-StoriesDevious\\Dev\\BSA\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Stories\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SLSDDi_*.*','SLSDDI_*.*','bpwMatchCardScript.*']

    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\SexLab-StoriesDevious.esp\\"] = ['*.*']
    modassets["meshes\\actors\\character\\SL_Stories_Devious\\"] = ['*.*']
    modassets["meshes\\armor\\SL_Stories_Devious\\"] = ['*.*']
    modassets["meshes\\clutter\\SL_Stories_Devious\\"] = ['*.*']

    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\SexLab-StoriesDevious.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\SL_Stories_Devious\\"] = ['*.*']
    modassets["textures\\armor\\SL_Stories_Devious\\"] = ['*.*']
    modassets["textures\\clutter\\SL_Stories_Devious\\"] = ['*.*']
    modassets["textures\\clutter\\cubemaps\\"] = ['bronze_e.dds', 'ore_quicksilver_e.dds', 'ore_steel_e.dds', 'shinyglass_e.dds']
    modassets["textures\\Milk\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-StoriesDevious\\Dev\\Loose\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Stories\\Data\\"

    modassets = {}
    modassets["textures\\actors\\character\\slavetats\\milkfarm\\"] = ['*.*']
    modassets["textures\\actors\\character\\slavetats\\"] = ['milkfarm.json']
    modassets["SEQ\\"] = ['SexLab-StoriesDevious.seq']
    modassets[""] = ['SexLab-StoriesDevious.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployStoriesDeviousVoicePack():
    print("========= Stories Devious Voice Pack")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-StoriesDevious\\Dev\\StoriesDeviousVoicePack\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Stories\\Data\\"

    modassets = {}

    modassets["sound\\Voice\\SexLab-StoriesDevious.esp\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployPatches():
    print("========= Patches")
    print("===== Sexlab Warm Bodies")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Obscure-patches\\SexLabWarmBodiesPatch\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\SexLabWarmBodiesPatch\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['_slff_playerAlias*.*','questVersioning.*','questVersioningPlayerAlias.*']
    modassets[""] = ['SexLab Warmbodies.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("===== Puppet Master")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Obscure-patches\\PuppetMasterPatch\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\PuppetMasterPatch\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['_mindconfig*.*','_mindscript.*']
    modassets[""] = ['PuppetMaster.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("===== Lovers Comfort")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Obscure-patches\\LoversComfortPatch\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\LoversComfortPatch\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['loverscomfort*.*','loverscomfort.*']
    modassets[""] = ['LoversComfort.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("===== College Days of Winterhold")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Obscure-patches\\CollegeDaysPatch\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\CollegeDaysPatch\\Data\\"

    modassets = {} 
    modassets[""] = ['CollegeDaysWinterhold.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("===== YPS Fashion")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Obscure-patches\\YPSFashionPatch\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\YPSFashionPatch\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['ypsPiercingTicker.*','ypsHairScript.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("===== Bathing in Skyrim")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Obscure-patches\\BathingInSkyrim\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\BathingInSkyrim\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['mzinBathePlayerAlias.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("===== Wolfclub")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Obscure-patches\\Wolfclub\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\Wolfclub\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['tif__05007b15.*','pchs*.*']
    modassets[""] = ["wolfclub.esp"]

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("===== Redbag Rorikstead")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Obscure-patches\\RedbagRoriksteadPatch\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\RedbagRoriksteadPatch\\Data\\"

    modassets = {}
    modassets["meshes\\rbroriksteadmeshes\\"] = ['*.*']
    modassets["textures\\RBRoriksteadTextures\\"] = ['*.*']
    modassets[""] = ["RedBag's Rorikstead.esp"]

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


    print("===== Border Hold Guards")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Obscure-patches\\BorderHoldGuards\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\BorderHoldGuards\\Data\\"

    modassets = {}
    modassets[""] = ["Hold Border Guards Anniversary.esp"]

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)



def deploySkyrimImmersionPatch():
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    print("===== Skyrim Immersion Patch")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SkyrimImmersionPatch\\Dev\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\SkyrimImmersionPatch\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SIP_*.*']
    modassets["meshes\\clutter\\SIP\\"] = ['*.*']
    modassets["textures\\clutter\\SIP\\"] = ['*.*']
    modassets[""] = ['SkyrimImmersionPatch.esp', 'SkyrimImmersionPatch-Legendary.esp', 'SkyrimImmersionPatch-ESO.esp', 'SkyrimImmersionPatch-seasons.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    sourcefolder = "G:\\Games-data\\custom mods\\02 - Releases\\SkyrimImmersionPatch\\Dev\\"
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SkyrimImmersionPatch\\Prod\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\SkyrimImmersionPatch\\"

    modassets = {}
    modassets[""] = ['ChangeLog.md']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployRunicENBReshade():
    print("========= ENB / ReShade visuals")
    print("===== Backup first")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\RunicENBReshade\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\RunicENBReshade\\ENB\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\RunicENBReshade\\ENB\\"

    modassets = {}
    modassets["enbseries\\"] = ['*.*']
    modassets[""] = ['enblocal.ini','enbseries.ini']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("===== Reshade")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\RunicENBReshade\\ReShade\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\RunicENBReshade\\ReShade\\"

    modassets = {}
    modassets[""] = ['RunicReShade.ini']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployTheWitcher3mods():
    print("========= The Witcher 3")
    sourcefolder = "F:\\Steam\\steamapps\\common\\The Witcher 3\\Mods\\modLongJourneyExtended\\content\\scripts\\game\\gameplay\\fast_travel_entities"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\TW3-LongJourneyExtendedPatch\\modLongJourneyExtended\\content\\scripts\\game\\gameplay\\fast_travel_entities"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\TW3-LongJourneyExtendedPatch\\modLongJourneyExtended\\content\\scripts\\game\\gameplay\\fast_travel_entities"

    modassets = {}
    modassets[""] = ['fastTravelEntity.ws']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    sourcefolder = "F:\\Steam\\steamapps\\common\\The Witcher 3\\Mods\\modLongJourneyExtended\\content\\scripts\\game\\gui\\menus"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\TW3-LongJourneyExtendedPatch\\modLongJourneyExtended\\content\\scripts\\game\\gui\\menus"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\TW3-LongJourneyExtendedPatch\\modLongJourneyExtended\\content\\scripts\\game\\gui\\menus"

    modassets = {}
    modassets[""] = ['mapMenu.ws']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    sourcefolder = "F:\\Steam\\steamapps\\common\\The Witcher 3\\Mods\\modLongJourneyExtended\\content\\scripts\\game\\player"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\TW3-LongJourneyExtendedPatch\\modLongJourneyExtended\\content\\scripts\\game\\player"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\TW3-LongJourneyExtendedPatch\\modLongJourneyExtended\\content\\scripts\\game\\player"

    modassets = {}
    modassets[""] = ['r4Player.ws']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    sourcefolder = "F:\\Steam\\steamapps\\common\\The Witcher 3\\Mods\\modLongJourneyExtended\\content\\scripts\\local"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\TW3-LongJourneyExtendedPatch\\modLongJourneyExtended\\content\\scripts\\local"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\TW3-LongJourneyExtendedPatch\\modLongJourneyExtended\\content\\scripts\\local"

    modassets = {}
    modassets[""] = ['RouteCheck.ws']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


def deployCyberpunk2077mods():
    print("========= Cyberpunk 2077")
    print("===== Limited Encumbrance")
    sourcefolder = "F:\\Steam\\steamapps\\common\\Cyberpunk 2077\\r6\\scripts\\LimitedEncumbrance"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Cyberpunk2077\\LimitedEncumbrance\\r6\\scripts\\LimitedEncumbrance"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\Cyberpunk2077\\LimitedEncumbrance\\r6\\scripts\\LimitedEncumbrance"

    modassets = {}
    modassets[""] = ['LimitedEncumbrance.reds', 'LimitedEncumbranceText.reds', 'Config.reds']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("===== Claim Vehicles")
    sourcefolder = "F:\\Steam\\steamapps\\common\\Cyberpunk 2077\\r6\\scripts\\ClaimVehicles"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Cyberpunk2077\\ClaimVehicles\\r6\\scripts\\ClaimVehicles"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\Cyberpunk2077\\ClaimVehicles\\r6\\scripts\\ClaimVehicles"

    modassets = {}
    modassets[""] = ['ClaimVehicles.reds', 'Config.reds']
    
    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    sourcefolder = "F:\\Steam\\steamapps\\common\\Cyberpunk 2077\\r6\\tweaks\\ClaimVehicles"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Cyberpunk2077\\ClaimVehicles\\r6\\tweaks\\ClaimVehicles"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\Cyberpunk2077\\ClaimVehicles\\r6\\tweaks\\ClaimVehicles"

    modassets = {}
    modassets[""] = ['missingcars_tweakxl.yaml']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    print("===== Immersion Patch")
    sourcefolder = "F:\\Steam\\steamapps\\common\\Cyberpunk 2077\\r6\\scripts\\ImmersionPatch"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Cyberpunk2077\\adaptiveSliders\\r6\\scripts\\ImmersionPatch"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\Cyberpunk2077\\ImmersionPatch\\r6\\scripts\\ImmersionPatch"

    modassets = {}
    modassets[""] = ['adaptiveSliders.reds']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Cyberpunk2077\\vehicleFastTravel\\r6\\scripts\\ImmersionPatch"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\Cyberpunk2077\\ImmersionPatch\\r6\\scripts\\ImmersionPatch"

    modassets = {}
    modassets[""] = ['vehicleFastTravel.reds']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


if __name__ == '__main__':
    with open('mods_manifest.json', 'r') as f:
        mods_data = json.load(f)

    # creating set of keys that we want to compare
    root_keys_check = set(["mod_groups"]) 
    
    if root_keys_check.issubset(mods_data.keys()):
        deployAllMods(mods_data)       
        # deployMod(mods_data, 'MOD UTILITIES', 'CKTOOLS')
        # deployModGroup(mods_data, 'MOD UTILITIES')

    else:
        print(">>>Error: Key mod_groups is missing from mods_manifest.json file")
            


