# This script will copy files from a source directory (skyrim/Data folder) to two target directories: one for backups and preparing BSA files and one for source control (github)

# Code adapted from: https://gist.github.com/Sleepingwell/6070119

# QUICK REFERENCES to Python resources
# https://docs.python.org/2/library/shutil.html
# https://www.pythonforbeginners.com/os/python-the-shutil-module
# http://xahlee.info/python/python_path_manipulation.html

import re
import os
import os.path
import shutil
import fnmatch
import filecmp



def join(*args):
    return os.path.normpath(os.path.join(*args))


def trymakedir(path):
    try:
        os.makedirs(path)
    except Exception as e:
        # print(e)
        if not os.path.exists(path):
            raise Exception('failed to create output directory: ' + path)


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
                                foundfiles = foundfiles + "\n" + "Updating file " + join(targetdir, fn)
                                copyfileflag = True
                            elif (((".esp" in fn) or (".esm" in fn)) and (not filecmp.cmp(join(root, fn), join(targetdir, fn)))):
                                foundfiles = foundfiles + "\n" + "Updating file " + join(targetdir, fn)
                                copyfileflag = True

                    if (copyfileflag):
                        shutil.copy(join(root, fn), join(targetdir, fn))
                        filecount = filecount + 1
        totalfilecount = totalfilecount + filecount
        if filecount != 0:
            print("----")
            print("Processing... " + pattern + " To: " + outputdir + foundfiles)
            print("     " + str(filecount) + " files in " + root)



def deployfiles(sourcelist, destinationlist, modassetslist):
    for asset in modassetslist.keys():
        filepatternlist = modassetslist[asset]
        for source in sourcelist:
            for destination in destinationlist:
                for filepattern in filepatternlist:
                    trymakedir(destination)
                    docopy(source + asset, destination + asset, filepattern)


def deployCKTools():
    print("========= CKTools")
    sourcefolder = "E:\\Documents\\Source\\CKTools\\"
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\CKTools\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\CKTools\\"

    modassets = {}
    modassets["DeployCKFiles\\"] = ['deployCkFiles.py']
    modassets["GetGithubReleases\\"] = ['getGithubReleases.py']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


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
    # modassets["meshes\\actors\\atronachflame\\"] = ['testfireatronach.nif']
    # modassets["meshes\\actors\\atronachflame\\character assets\\"] = ['*.*']
    #  modassets["meshes\\actors\\canine\\"] = ['compressleveloverride.txt', 'dogstatic.nif', 'nocompressionoverride.txt', 'spublocksize.txt']
    #  modassets["meshes\\actors\\canine\\character assets dog\\"] = ['skeleton.nif']
    #  modassets["meshes\\actors\\canine\\character assets wolf\\"] = ['skeleton.nif']
    # modassets["meshes\\actors\\chaurus\\"] = ['testchaurus.nif']
    # modassets["meshes\\actors\\chaurus\\character assets\\"] = ['skeleton.nif']
    # modassets["meshes\\actors\\falmer\\"] = ['falmerarmorstatic.nif', 'falmerstatic.nif']
    # modassets["meshes\\actors\\falmer\\character assets\\"] = ['skeleton.nif']
    # modassets["meshes\\actors\\spriggan\\"] = ['fxsprigganattachments.nif', 'fxsprigganattachmentsmatron.nif', 'fxsprigganswarm.nif', 'sprigganfxtestunified.nif']
    # modassets["meshes\\actors\\spriggan\\character assets\\"] = ['skeleton.nif']
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

    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\SexLab_Hormones.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\Rosa\\"] = ['*.*']
    modassets["textures\\actors\\character\\SL_Hormones\\"] = ['*.*']
    modassets["textures\\clutter\\SL_Hormones\\"] = ['*.*']
    modassets["textures\\_SLH\\"] = ['*.*']
    modassets["textures\\baronb\\dragon\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-Hormones\\Dev\\Loose\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Hormones\\Data\\"

    modassets = {}
    modassets["Interface\\SexLab_Hormones\\"] = ['logo.dds']
    modassets["SEQ\\"] = ['SexLab_Hormones.seq']
    modassets["textures\\actors\\character\\slavetats\\bimbo\\"] = ['*.*']
    modassets["textures\\actors\\character\\slavetats\\"] = ['bimbo.json']
    modassets[""] = ['SexLab_Hormones.esp']

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
    modassets["textures\\TeraArmorsM\\castanic_f_r16\\"] = ['*.*']
    modassets["textures\\TeraArmorsM\\xTeraglassrobe\\"] = ['*.*']
    modassets["textures\\TeraArmorsM\\zzterah21\\"] = ['*.*']
    modassets["textures\\zaz\\xxfurotrap\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\Kyne-Blessing\\Dev\\Loose\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Parasites\\Data\\"

    modassets = {}
    modassets["Interface\\KyneBlessing\\"] = ['logo.dds']
    modassets["SEQ\\"] = ['SexLab-Parasites.seq']
    modassets[""] = ['SexLab-Parasites.esp']

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
    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\Skyrim.esm\\"] = ['00013B9B.NIF', '000136BC.NIF']
    modassets["meshes\\actors\\character\\SL_Stories\\"] = ['*.*']
    modassets["meshes\\armor\\SL_Stories\\"] = ['*.*']
    modassets["meshes\\clutter\\SL_Stories\\"] = ['*.*']

    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\SexLab-Stories.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\Skyrim.esm\\"] = ['00013B9B.*', '000136BC.*']
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


def deployStoriesDevious():
    print("========= Stories Devious")
    sourcefolder = "F:\\Steam\\steamapps\\common\\skyrim\\Data\\"

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-StoriesDevious\\Dev\\BSA\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Stories\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SLSDDi_*.*']

    modassets["meshes\\actors\\character\\FacegenData\\FaceGeom\\SexLab-StoriesDevious.esp\\"] = ['*.*']
    modassets["meshes\\actors\\character\\SL_Stories_Devious\\"] = ['*.*']
    modassets["meshes\\armor\\SL_Stories_Devious\\"] = ['*.*']
    modassets["meshes\\clutter\\SL_Stories_Devious\\"] = ['*.*']

    modassets["textures\\actors\\character\\FacegenData\\FaceTint\\SexLab-StoriesDevious.esp\\"] = ['*.*']
    modassets["textures\\actors\\character\\SL_Stories_Devious\\"] = ['*.*']
    modassets["textures\\armor\\SL_Stories_Devious\\"] = ['*.*']
    modassets["textures\\clutter\\SL_Stories_Devious\\"] = ['*.*']
    modassets["textures\\clutter\\cubemaps\\"] = ['bronze_e.dds', 'ore_quicksilver_e.dds', 'ore_steel_e.dds', 'shinyglass_e.dds']
    modassets["textures\\clutter\\Milk\\"] = ['*.*']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SexLab-StoriesDevious\\Dev\\Loose\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLmods\\Stories\\Data\\"

    modassets = {}
    modassets["SEQ\\"] = ['SexLab-StoriesDevious.seq']
    modassets[""] = ['SexLab-StoriesDevious.esp']

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

    print("===== Skyrim Immersion Patch")
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SkyrimImmersionPatch\\Dev\\Data\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\SkyrimImmersionPatch\\Data\\"

    modassets = {}
    modassets["scripts\\"] = ['SIP_*.*']
    modassets[""] = ['SkyrimImmersionPatch.esp']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)

    sourcefolder = "G:\\Games-data\\custom mods\\02 - Releases\\SkyrimImmersionPatch\\Dev\\"
    targetfolder = "G:\\Games-data\\custom mods\\02 - Releases\\SkyrimImmersionPatch\\Prod\\"
    githubfolder = "G:\\Games-data\\custom mods\\03 - Github\\SkyrimLL\\SkLLpatches\\SkyrimImmersionPatch\\"

    modassets = {}
    modassets[""] = ['ChangeLog.md']

    deployfiles([sourcefolder], [targetfolder, githubfolder], modassets)


if __name__ == '__main__':

    # ===== CK Tools
    deployCKTools()

    # ===== Sanguine Debauchery +
    deploySD()

    # ===== SL Dialogues
    deploySLD()

    # ===== Sisterhood of Dibella
    deploySLSD()

    # ===== Alicia
    deployAlicia()

    # ===== Hormones
    deployHormones()

    # ===== Parasites
    deployParasites()

    # ===== Mind Control
    deployMindControl()

    # ===== Family Ties
    deployFamilyTies()

    # ===== Stories
    deployStories()
    deployStoriesDevious()

    # ===== Obscure Patches
    deployPatches()