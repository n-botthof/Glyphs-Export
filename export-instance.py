# MenuTitle: Export with Version Number
# -*- coding: utf-8 -*-

# This script exports OTF files of all active instances to a specified export folder and copys them to InDesign’s font folder.
#
# The OTF files’ names contain metadata about the export. 
# The copies in InDesign’s folder only contain the font family’s and the instance’s names, and are overwritten at every invocation.
#
# The path to the export folder and the InDesign folder can easily be modified.


import os
from shutil import copyfile
from datetime import datetime


the_font = Glyphs.font

# here are my glyph files
production_folder = os.path.dirname(the_font.filepath)

# this is where I archive my exported files
export_folder = os.path.join(os.path.split(production_folder)[0], "Export/")

# InDesign’s font folder
inDesign_folder = "/Applications/Adobe InDesign CC 2019/Fonts"


font_name = the_font.familyName
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

for instance in the_font.instances:
	if instance.active:

		# export to export folder
		file_name = "{}-{} {} {}.{:03}.otf".format(font_name, instance.name, timestamp, the_font.versionMajor, the_font.versionMinor)
		export_path = os.path.join(export_folder, file_name)
		instance.generate(FontPath = export_path, AutoHint = False)

		# export to InDesign folder
		file_name = "{}-{}.otf".format(font_name, instance.name)
		inDesign_path = os.path.join(inDesign_folder, file_name)
		copyfile(export_path, inDesign_path)


Glyphs.showNotification("Export Fonts", "done exporting {}".format(Glyphs.font.familyName))

