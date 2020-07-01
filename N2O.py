# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 13:34:37 2020

@author: books
"""

from os import makedirs, path
from re import sub
from shutil import copyfileobj, make_archive
from zipfile import ZipFile
from pathlib import Path
import N2Omodule
from tempfile import TemporaryDirectory
from easygui import fileopenbox


NotionZip = Path(fileopenbox())
# NotionZip = Path(r'D:\Box Sync\Gpython\Notion2Obsidian-20200617\NotionExport-orig-minimal.zip')


# Load zip file
notionsData = ZipFile(NotionZip, 'r')

NotionPathRaw = []
ObsidianPathRaw = []
NotionPaths = []
ObsidianPaths = []



# Generate a list of file paths for all zip content
[NotionPathRaw.append(line.rstrip()) for line in notionsData.namelist()]
# [print(l[0],l[1]) for l in enumerate(NotionPaths)]



# Clean paths for Obsidian destination
regexUID = "\s\w{32}"
for line in NotionPathRaw:
    ObsidianPathRaw.append(sub(regexUID, "", line))
# [print(l[0],l[1]) for l in enumerate(ObsidianPaths)]


### PATHS IN PROPER OS FORM BY PATHLIB ###
[NotionPaths.append(Path(line)) for line in NotionPathRaw]
[ObsidianPaths.append(Path(line)) for line in ObsidianPathRaw]



# Get all the relevant indices (folders, .md, .csv, others)
mdIndex, csvIndex, othersIndex, folderIndex, folderTree = N2Omodule.ObsIndex(ObsidianPaths)
 

# Rename the .csv files to .md files for the conversion
for i in csvIndex:
    ObsidianPaths[i] = Path(str(ObsidianPaths[i])[0:-3]+"md")
# [print(ObsidianPaths[i]) for i in csvIndex]


## Create a temporary directory to work with
unzipt = TemporaryDirectory()
tempPath = Path(unzipt.name)
# print('tempPath',tempPath)


## Create temp directory paths that match zip directory tree
tempDirectories = []

# Construct complete directory paths (<tempDirecory>/<zipDirectories>)
for d in folderTree:
    tempDirectories.append(tempPath / d)
# [print(l) for l in tempDirectories]

## Create the temporary directory structure for future archive
for d in tempDirectories:
    makedirs(d, exist_ok=True)






# Process all CSV files
for n in csvIndex:
    
    # Access the original CSV file
    with notionsData.open(NotionPathRaw[n], "r") as csvFile:
        # print("===",ObsidianPaths[n])
         
        # Convert CSV content into Obsidian Internal Links
        mdTitle = N2Omodule.N2Ocsv(csvFile)
    
        ## Make temp destination file path
        newfilepath = tempPath / ObsidianPaths[n]
        
        # Check if file exists, append if true
        if path.exists(newfilepath):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        
        # Save CSV internal links as new .md file
        with open(newfilepath, append_write) as tempFile:
            [print(line.rstrip(), file=tempFile) for line in mdTitle]
        
    ### This shows the contents of the saved test file!    
    # with open(newfilepath, "r") as f:
    #     print("from saved tempfile:")
    #     [print(line.rstrip()) for line in f]






# Process all MD files
for n in mdIndex:
    
    # Access the original MD file
    with notionsData.open(NotionPathRaw[n], "r") as mdFile:
        # [print(line.decode().rstrip()) for line in mdFile]
        
        # Find and convert Internal Links to Obsidian style
        mdContent = N2Omodule.N2Omd(mdFile)
        # [print(l)for l in mdContent]
        
        ## Make temp destination file path
        newfilepath = tempPath / ObsidianPaths[n]
        # print(newfilepath)
        
        # Check if file exists, append if true
        if path.exists(newfilepath):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        # print(append_write)
        
        # Save modified content as new .md file
        with open(newfilepath, append_write, encoding='utf-8') as tempFile:
            [print(line.rstrip(), file=tempFile) for line in mdContent]
        


    ### This check just shows the contents of the saved test file!    
    # with open(newfilepath, "r", encoding='utf-8') as f:
    #     print("from saved tempfile:")
    #     [print(line.rstrip()) for line in f]






#### Process all attachment files using othersIndex ####
for n in othersIndex:
    
    # Move the file from NotionPathRaw[n] in zip to newfilepath = tempPath / ObsidianPaths[n]
    newfilepath = tempPath / ObsidianPaths[n]
    # print('newfilepath:', newfilepath)
    
    with notionsData.open(NotionPathRaw[n]) as zf:
        with open(newfilepath, 'wb') as f:
            copyfileobj(zf, f)

    




# Save temporary file collection to new zip
make_archive( NotionZip.parent / (NotionZip.name[:-4]+'-ObsidianReady'), 'zip', tempPath)






# Check files in destination
# def tree2(directory):
#     print(f'+ {directory}')
#     for path in sorted(directory.rglob('*')):
#         depth = len(path.relative_to(directory).parts)
#         spacer = '    ' * depth
#         print(f'{spacer}+ {path.name}')
# tree2(tempPath)




# Close out!
notionsData.close()