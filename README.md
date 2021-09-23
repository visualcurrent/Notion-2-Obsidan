# Notion-2-Obsidian

For those considering switching from [Notion](https://www.notion.so/) to [Obsidian](https://obsidian.md/), here is a Python 3 script that converts your Notion export into an Obsidian friendly format.

When you run the N2O.py script, it will:
1. Launch an Open-File dialogue where you'll navigate to your Notion-Export.zip file
2. Convert all Internal Links in your Notion pages to an Obsidian friendly markdown format
3. Repackages all the files into a new zip archive that is Obsidian vault compatible

The script will leave your orginal Notion archive unmodified.

The resulting archive can be extracted and opened as, or added to, an Obsidian vault.

## The Problem with your Notion Export
Out of the box, the export files that Notion provides do not migrate to Obsidian very well. All external links will work, but:

- The hierarchical structure of your pages can only be navigated using Obsidian’s file explorer.
- None of the internal navigation links work, which also means there won’t be any backlinks or connections in Obsidian's Graph View.
- None of the content in your Notion tables will be viewable.
- Embedded images also won’t show.

All of this is remedied by this script. Note however, that Notion comments do NOT appear to be included in their export files.

## Methodology

If you're interested, the full sequence of modifications needed to make your Notion export compatible with Obsidian can be found in the write-up found in the [Methodology.md](METHODOLOGY.md) file in this git.

# Supporting the Work

I’m happy to offer you this script and the conversion methodology. If you're able and inclined, a donation for the convenience and time savings would be genuinely appreciated. There's a couple donation links at the bottom of this page.

I estimate that anyone using the [Methodology.md](METHODOLOGY.md) can convert their Notion export in a day or less of work. Without this guide, it would likely take several days of troubleshooting. If you’re a confident programmer, it may take you just a couple hours with the guide. I encourage everyone to go through the process. It is satisfying.

However, if your time is worth more spent elsewhere. Feel free to use the code and switch to Obsidian in mere seconds!

# Export Your Full Notion Database
If you haven't already, you'll need to export your content from Notion.

1.  From your Notion app, click the **Settings & Members** tab in the sidebar
![Settings&Members](media/export1.png)
2.  Find and click the **Settings** tab. Find the **Export content** section. Click the **Export all workspace content** button
![Settings](media/export2.png)
3.  Select **Markdown & CSV** as Export Format and click the **Export** button
![Export](media/export3.png)
4.  Save the resulting .zip file to your computer
5.  Extract the .zip contents to a known location

# Run the N2O.py Script
- Make sure `N2O.py` and `N2Omodule.py` are in the same directory.
- Run `Python3 N2O.py`
- Use the Open-File dialog that pops up to navigate to your NotionExport.zip file.
- When the script finishes you'll find a new zip file in the same directory that's ready for Obsidian.

# Importing or Integrating into Obsidian

Time to import everything into Obsidian

1.  Place all the converted files into a directory of your choosing
2.  Open Obsidian and click the Vault Icon ![vault icon](media/vaulticon.png)
3.  Select **Open folder as vault**
![open vault](media/vault.png)
4.  Use the Select Folder window to navigate to the directory with your newly converted files

Enjoy the shift to Obsidian!

# Donation Links
If the instructions or code have been useful for you, please consider the time you've saved and treat me to half a lunch or so :)  My hole-in-the-bucket Covid-19 era income would greatly appreciate it.

Here are some donation links for me:
* PayPal: https://www.paypal.me/GabrielKrause
* Venmo: @Gabriel-Krause
* Etherium: 0xeAE10E05427845aE816E61605eCC779A2d5e59A4

# FAQ
## ModuleNotFoundError: No module named 'easygui'
You don't have the easygui module installed locally.

You can first create a lil virtual environment to keep your base system clean:
```
$ python3 -m venv ~/.venv/n2o
$ source ~/.venv/n2o/bin/activate
```

After that (or without it) you can install this module locally by running the following command:
```
$ pip install -r requirements.txt
```

## ImportError: Unable to find tkinter package.
Tkinter is a little tricker to install, it requires your python installation to include it natively.

If you're on MacOS, you can install a python distribution which supports tkinter:
```
$ brew install python-tk
```
