# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 14:16:18 2020

@author: books
"""

from io import TextIOWrapper
from os import path
from re import compile, search
from csv import DictReader
from pathlib import Path


def ObsIndex(contents):
    """
    Function to return all the relevant indices 
    Requires: contents are pre-conditioned by pathlib.Path()
    Returns: (mdIndex, csvIndex, othersIndex, folderIndex, folderTree)
    """
    
    ## index the directory structure
    folderIndex = []
    folderTree = []

    for line in enumerate(contents):
        if not line[1].suffix:
            folderIndex.append(line[0]) #save index
            folderTree.append(line[1])
    ## Case: directories are implicit
    if not folderIndex:
        Tree = list(set([path.dirname(x) for x in contents]))
        [folderTree.append(Path(l)) for l in Tree]

    
    ## Index the .md files
    mdIndex = []
    for line in enumerate(contents):
        if line[1].suffix == ".md":
            mdIndex.append(line[0]) #save index
    
    
    ## Index the .csv files
    csvIndex = []
    for line in enumerate(contents):
        if line[1].suffix == ".csv":
            csvIndex.append(line[0]) #save index

    
    ## index the other files using set difference
    othersIndex = list(set(range(0,len(contents)))
        - (set(folderIndex)|set(mdIndex)|set(csvIndex)))
    
    return mdIndex, csvIndex, othersIndex, folderIndex, folderTree


def N2Ocsv(csvFile):
    
    # Convert csv to dictionary object
    reader = DictReader(TextIOWrapper(csvFile, "utf-8-sig"), delimiter=',', quotechar='"')
   
    dictionry = {}
    for row in reader: # I don't know how this works but it does what I want
        for column, value in row.items():
            dictionry.setdefault(column, []).append(value)
           
    IntLinks = list(dictionry.keys())[0] # Only want 1st column header    
    oldTitle = dictionry.get(IntLinks)

    Title = []
    mdTitle = []

    # Clean Internal Links
    regexURLid = compile("(?:https?|ftp):\/\/")
    regexSymbols = compile("[^\w\s]")
    regexSpaces = compile("\s+")

    for line in oldTitle:
        line = line.rstrip()
        #1 Replace URL identifiers and/or symbols with a space
        line = regexURLid.sub(" ",line)
        line = regexSymbols.sub(" ",line)
         #2 Remove duplicate spaces
        line = regexSpaces.sub(" ", line)        
        #3 Remove any spaces at beginning
        line = line.lstrip()
        #4 Cut title at 50 characters
        line = str(line)[0:50]
        #5 Remove any spaces at end
        line = line.rstrip()    
        if line:
            Title.append(line)
    
    ## convert Titles to [[internal link]]
    for line in Title:
        mdTitle.append("[["+line+"]] ")
    
    return mdTitle


def convertInternalLink(matchObj):
# converts Notion Internal links (found by regex) to Obsidian pretty links

    regexSymbols = compile("[^\w\s]")
    regexSpaces = compile("\s+")

    userTitle = matchObj.group(1)
    ExternalURL = matchObj.group(2)
    urlTitle = matchObj.group(3)
    
    # Replace symbols with space
    urlTitle = regexSymbols.sub(" ",urlTitle)
    
    # Remove duplicate spaces
    urlTitle = regexSpaces.sub(" ",urlTitle)

    # Cut title at 50 characters
    urlTitle = urlTitle[0:50]
    
    # Remove any spaces at end
    urlTitle = urlTitle.rstrip()
   
    # Reconstruct Internal Links as pretty links and source footnote
    if urlTitle == userTitle:
        PrettyLink = "[["+urlTitle+"]] ^["+ExternalURL+"] "
    else:
        PrettyLink = "[["+urlTitle+"|"+userTitle+"]] ^["+ExternalURL+"] "

    # Substitute regex find with PrettyLink
    return PrettyLink

def convertBlankLink(matchObj):
# converts Notion about:blank links (found by regex) to Obsidian pretty links

    regexSymbols = compile("[^\w\s]")
    regexSpaces = compile("\s+")
    
    InternalTitle = matchObj.group(1)
    
    # Replace symbols with space
    InternalLink = regexSymbols.sub(" ",InternalTitle)
    
    # Remove duplicate spaces
    InternalLink = regexSpaces.sub( " ", InternalLink)
    
    # Remove any spaces at beginning
    InternalLink = InternalLink.lstrip()
    
    # Cut title at 50 characters
    InternalLink = InternalLink[0:50]
    
    # Remove any spaces at end
    InternalLink = InternalLink.rstrip()
    
    # Reconstruct Internal Links as pretty links
    PrettyLink = "[["+InternalLink+"]] "
    
    # Substitute regex find with PrettyLink
    return PrettyLink
    
    
    

def N2Omd(mdFile):
    # Local Dependancies: convertInternalLink(), convertBlankLink()
    
    newLines = []
    
    for line in mdFile:
        line = line.decode("utf-8").rstrip()
    
  
        
  
    # folder style links
        regexPath =     compile("^\[(.+)\]\(([^\(]*)(?:\.md|\.csv)\)$")
        regexUID =      compile("%20\w{32}")
        regex20 =       compile("%20")
        regexSlash =    compile("\s\/")
        
        # Identify and group relative paths
        pathMatch = regexPath.search(line)
        # modify paths into local links. just remove UID and convert spaces
        if pathMatch:
            Title = pathMatch.group(1)
            relativePath = pathMatch.group(2)
            # Clean UID
            relativePath = regexUID.sub(" ",relativePath)
            # correct spaces
            relativePath = regex20.sub(" ",relativePath)
            relativePath = regexSlash.sub("/",relativePath).strip()
            
            # Reconstruct Links as pretty links
            if relativePath == Title:
                PrettyLink = "[["+relativePath+"]] "
            else:
                PrettyLink = "[["+relativePath+"|"+Title+"]] "
                
            line = PrettyLink
        
        
        
        
        
        # Internal style links. 
        ## Group1:Pretty Link Title 
        ## Group2: URL. 
        ## Group3: target file name (in web form but not in exported form without symbols) 
        regexInternalLink = compile("\[(.[^\[\]\(\)]*)\]\((https:\/\/www.notion.so\/(?:.[^\/]*)\/(.[^\[\]\(\)]*)-.[^\[\]\(\)]*)\)")
        
        match = regexInternalLink.search(line)
        # Substitute regex find with PrettyLink
        if match:
            line = regexInternalLink.sub(convertInternalLink, line)       

        
        
        
        
        # about:blank links (lost or missing links within Notion)
        ## Group1:Pretty Link Title
        regexBlankLink = compile("\[(.[^\[\]\(\)]*)\]\(about:blank#.[^\[\]\(\)]*\)")
        
        matchBlank = regexBlankLink.search(line) 
        if matchBlank:
            line = regexBlankLink.sub(convertBlankLink, line)
        
        

        
        
        # Embedded attachment links
        regexAttached = compile("!\[(.[^\[\]\(\)]*)\]\((.[^\[\]\(\)]*)\)")
        regexUID =      compile("%20\w{32}")
        regex20 =       compile("%20")
        regexSlash =    compile("\s\/")

        matchAttach = regexAttached.search(line)
        if matchAttach:
            attachment = matchAttach.group(1)
            # Clean UID
            attachment = regexUID.sub(" ",attachment)
            # correct spaces
            attachment = regex20.sub(" ",attachment)
            attachment = regexSlash.sub("/",attachment).strip()
            
            # Reconstruct Links as embedded links
            embededLink = "![["+attachment+"]] "

            line = regexAttached.sub(embededLink, line)              
        
        
        # Convert tags after lines starting with "Tags:"
        regexTags = "^Tags:\s(.+)"
        
         # Search for Internal Links. Will give match.group(1) & match.group(2)
        tagMatch = search(regexTags,line)
        
        Otags = []
        if tagMatch:
            Ntags = tagMatch.group(1).split(",")
            for t in enumerate(Ntags):
                Otags.append("#"+t[1].strip())

            line = "Tags: "+", ".join(Otags)
    

        newLines.append(line)
    
    return newLines

    
    