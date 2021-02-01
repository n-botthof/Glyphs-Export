# MenuTitle: Export with Version Number 2
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
date = datetime.now().strftime('%Y-%m-%d')
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
print(timestamp)

if os.path.isdir(os.path.join(export_folder, date)) == False:
	os.mkdir(os.path.join(export_folder, date))

for instance in the_font.instances:

	# export to export folder
	if instance.active:
		export_path = os.path.join(export_folder, date)
		instance.generate(FontPath = export_path, AutoHint = False)

		# export to InDesign folder
		file_name = "{}-{}.otf".format(font_name, instance.name)
		export_path_name = export_path + "/" + file_name
		print(export_path)
		print(export_path_name)
		#check if there is already a project folder inside the indesignfolder
		if os.path.isdir(os.path.join(inDesign_folder, font_name)) == False:
			os.mkdir(os.path.join(inDesign_folder, font_name))
		#copy into this folder in indesign
		inDesign_path = os.path.join(inDesign_folder ,font_name, file_name)
		copyfile(export_path_name, inDesign_path)

# check if there is an Archive, if not create it
if os.path.isdir(os.path.join(export_folder, "Archive")) == False:
	os.mkdir(os.path.join(export_folder, "Archive"))

original_fontname = font_name
the_font.familyName = original_fontname + "_" + timestamp

for instance in the_font.instances:
	archive_path = os.path.join(export_folder, "Archive")
	instance.generate(FontPath = archive_path, AutoHint = False)

the_font.familyName = original_fontname

Glyphs.showNotification("Export Fonts", "Done exporting and archiving {}".format(Glyphs.font.familyName))