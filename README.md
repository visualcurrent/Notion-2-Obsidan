# Notion-2-Obsidan
Conversion routines to convert all Notion .md exports to full Obsidian compatibility

For those considering switching from [<span class="underline">Notion</span>](https://www.notion.so/) to [<span class="underline">Obsidian</span>](https://obsidian.md/), here is a full sequence of modifications to make your Notion export compatible with Obsidian.

Out of the box, the export files that Notion provides do not migrate to Obsidian well. The hierarchical structure is preserved and all your work can be navigated and viewed using Obsidian’s file explorer. Any of your external links will be available. However, none of the internal navigation links will work, which also means there won’t be any backlinks, which is one of the great features of Obsidian. Embedded images also won’t show.

I’m using the Windows OS. Other OS users will want to substitute the tools suggested below for ones compatible on your system. [<span class="underline">Alternativeto.net</span>](https://alternativeto.net/) is a great resource to find what you need.

Note that Notion comments do NOT appear to be included in their export files.

Outside of missing comments. This guide will give you full internal link and backlink integration for your content in Obsidian.

# Supporting the Work

I’m happy to offer you the complete process for your content migration to Obsidian. I’ve been diligent in documenting all the needed steps and they should save you considerable time and frustration.

Should you want to save even more time, I have wrapped this process into a small program that will convert all of your links and files to Obsidian in a matter of seconds. For a sliding scale donation starting at $4 USD, you can have the full conversion tool.

I estimate that anyone using this guide can convert their Notion export in a day or less of work. Without this free guide, it would likely take several days of troubleshooting. If you’re a confident programmer, it may take a couple hours with this guide. I encourage everyone to go through the process. It is rather satisfying.

However, if your time is worth more spent elsewhere, consider what the time savings is worth to you. My hole-in-the-bucket COVID-19 era income will greatly appreciate the help.

Otherwise, let’s get started\! Here are the steps...

# Export Your Full Notion Database

1.  > From your Notion app, click the **Settings & Members** tab in the sidebar  
    > ![](media/image2.png)

2.  > Find and click the **Settings** tab. Find the **Export content** section. Click the **Export all workspace content** button  
    > ![](media/image1.png)

3.  > Select **Markdown & CSV** as Export Format and click the **Export** button  
    > ![](media/image4.png)

4.  > Save the resulting .zip file to your computer

5.  > Extract the .zip contents to a known location

# Remove the UID from all files and folders

All user-generated content will show a 32 digit alphanumeric Unique Identifier (UID).

They look like this:

> Meeting Notes 38f9b024692a4d0fbc14088d47c72d67  
> Random Notes 49330b16a1f54b4d92b442b25ea986de.md

We’ll want to remove these UIDs from all of your files and folders.

Use a file renaming tool like [<span class="underline">ReNamer</span>](http://www.den4b.com/products/renamer) to remove the last 33 characters (UID + space) of every file and folder.

## Duplicate filenames

Notion differentiates notes with the UID which allows their users to work with multiple notes with the same filename. Since we can’t have multiple files with the same name in our operating system, a reasonable solution to this is to combine the contents of files having the same name within a common directory.

# Convert Notion Style Links to Obsidian Style Links

Any file in the export package may have links that need conversion to an Obsidian format. A good search and replace tool that’s capable of batch processing multiple files will make this work much easier. I’ve found [<span class="underline">notepad++</span>](https://notepad-plus-plus.org/) to be great for this. Use whatever works for you.

## Process the .MD Files

### Convert Internal links to Obsidian format 

There will be four types of links in the exported files to process. When exported from Notion, they are all in the same "inline" wiki link format. But they differ enough to confidently identify and batch process each type with your search and replace tools.

### External Links

Notion and Obsidian use the same format for external links. These links should be left alone. They look like this:

> \[Link Name\](http://external.web.address)

### User Generated Internal Links

These are links that the user had manually generated to tie notes together within Notion. They can be identified within your pages by the URL containing the notion domain and their username.

> \[Link Name\]([<span class="underline">https://notion.so/username/note\_name+UID</span>](https://notion.so/username/note_name+UID))

We’re primarily interested in the note filename so that we can build complete link and backlink threads between our content. But there’s also enough information in these links to build pretty links, and also maintain a URL link to the original content on the Notion servers. Here, I’ll be including the source link as a footnote, should you ever need the original reference. I originally built these in so that if a link didn’t work in obsidian, we could still find our content easily. So far all links have worked but we can keep the links as a simple, unobtrusive safeguard.

Process Link Names:

1.  > Isolate and save the {URL} portion

2.  > Isolate and save the {Link Name} portion

3.  > Isolate the {Note Name} portion to make it Obsidian friendly

4.  > Search and replace any symbols in the {Note Name} to a space. (Only alphanumerics, underscores, and spaces are retained in Notion exported filenames)

5.  > Remove any duplicate spaces and leading/trailing spaces from the {Note Name}

6.  > Reconstruct Internal Links as pretty links with the source URL as a footnote
    
    1.  > If {Link Name} is the same as {Note Name}  
        > \[\[Note Name\]\] ^\[URL\]
    
    2.  > If {Link Name} is different than {Note Name}  
        > \[\[Note Name|Link Name\]\] ^\[URL\]

### Structural Links

Many of the connections between pages in Notion are inferred by hierarchy. When exporting this shows up as a directory structure. When using Notion, there’s no obvious visual difference between a directory and a page that you've created. Directories render as if it was a normal page.

Notion exports a representational .md file for these directories (that simply look like a page in Notion). This file will exist as a sidecar file alongside its respective directory. It will also have the same name as its respective directory. This sidecar .md file contains relative links to all the contents within the directory. Once processed, these will provide uninterrupted threads between all of your content in Obsidian.

Note that some directories will have a sidecar .csv file instead of a sidecar .md file. Notion exports these when a full-page database has been created and contains no other content blocks besides the Table, Board, List, or Gallery. See the CSV conversion section below.

The relative links within these sidecar .md files are structured differently than user generated internal links. They each have their own line and follow this pattern:

> \[Note Title\](RelativePath+UID/filename+UID.fileExtension)

For example:

> \[Micronutrient Smoothie\](Bodywork%20731fe478ea6048e1ac0df8c7f7ed95bf/Micronutrient%20Smoothie%2021e2b0c0922d46f387c8b353a17ff734.md)

We want to preserve the relative path structure that these links contain. This helps mitigate the differences between how Notion and Obsidian deal with notes that have the same name.

Process the relative paths in each line, in this order:

1.  > Remove the UIDs and the single leading URL space encoding (%20) in front of the UIDs

2.  > Remove the file extension (.md or .csv)

3.  > Search and replace the all remaining URL space encoding characters (%20) with a normal space character

4.  > Remove parentheses

5.  > Restructure the links into Obsidian Pretty Link format  
    > \[\[Relative/Path/filename|Note Title\]\]  
    > \[\[Bodywork/Micronutrient Smoothie|Micronutrient Smoothie\]\]

### Broken Links

There may be broken links within Notion. Often a broken link in Notion still has an associated file. It’s worth capturing and converting any broken links. These links are easily identified by the about:blank\# string where a notion.io URL should be. Here are a couple examples:

> \[Evaluate on Tuesday\](about:blank\#Evaluate%20on%20Tuesday)  
> \[2017-1-15 19:14\](about:blank\#2017-1-15%2019%3A14)

Process the broken links:

1.  > Remove the URL section in parentheses

2.  > Only alphanumerics, underscores, and spaces are retained in Notion exported filenames. Convert all other symbols to a space

3.  > Replace duplicate spaces with a single space

4.  > Remove any leading or trailing spaces

5.  > Frame the modified title in Obsidian double square brackets

> \[\[Evaluate on Tuesday\]\]  
> \[\[2017 1 15 19 14\]\]

### Convert tags in lines starting with "Tags: "

Notion renders tags in the .md page exports on a single line starting with “Tags: ” near the top of a page.

Any words that follow will be separated with a comma.

> Tags: Routine, Structure

Each of these words should be converted to the Obsidian tag format.

1.  > Find all words after “Tags :”

2.  > Prefix each of them with a hash “\#”

> Tags: \#Routine, \#Structure

## Process the CSV files

Notion exports a CSV file for every Table, Board, List, or Gallery. The first column in each of these CSV files can be easily converted to an Internal Link for Obsidian.

### Delete all but the first column

Beyond the first Internal Link column, all the data in the following columns exist within the target file. Keeping the data here is liable to become a maintenance issue, as the additional data will not be mirrored between this table representation and the actual file content. Deleting all but the first column is suggested, but feel free to leave the redundant content if you don’t plan on changing the linked files or if there’s some other value.

### Modify Internal Links

Search and replace to modify the Internal Links in this order:

1.  > If there's a web link in the title, and the link includes URL identifier (http, https, ftp). It must be removed because Notion exports these pages without the URL identifier in the filename.

2.  > Only alphanumerics, underscores, and spaces are retained in Notion exported filenames. All other symbols need to be converted to a space.

3.  > Replace duplicate spaces with a single space.

4.  > Remove any leading spaces

5.  > Notion cuts all filenames to a maximum of 50 characters. So cut the title to 50 characters if it’s longer.

6.  > Finally, remove any trailing spaces.

Now that all the Internal Links match their respective file names, wrap each one in double square brackets to be an Obsidian Internal Link.

> \[\[filename1\]\]  
> \[\[filename2\]\]

### Rename CSV to MD

Once the Internal Links have been converted in a Notion CSV file, change the file extension to .md. Again, [<span class="underline">ReNamer</span>](http://www.den4b.com/products/renamer) can be used to streamline this step once all the content has been corrected.

# Final Steps

Nice work\! You’re finished. Time to import everything into Obsidian

1.  > Place all the converted files into a directory of your choosing

2.  > Open Obsidian and click the Vault Icon ![](media/image3.png)

3.  > Select **Open folder as vault**  
    > ![](media/image5.png)

4.  > Use the Select Folder window to navigate to the directory with your newly converted files

5.  > Enjoy the shift to Obsidian\!
