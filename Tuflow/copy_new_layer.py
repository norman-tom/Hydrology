"""
Author: Tom Norman

This is a script that copies the Tuflow GIS Empty files from the empty directoy to the working directory and renames them accordingly.
The new layer naming convention must follow the Tuflow naming convention so the script understands what file you want to copy.
Once the new GIS files are in the working directory these can be dragged into QGIS
The script needs to be placed in the "../empty" directory for example "~/tuflow/model/gis". This is the default working directory for GIS files.
The empty path can be modified if this is not the case. 
"""

import os
import shutil

dirname = os.path.dirname(__file__)

def main():
    _sentinal = "_empty_"
    _layer = ""
    _empties_name = []
    _tags = []
    _types = []
    _extensions = []
    #Modify this path if your file structure differs from the default
    _empty_dir = os.path.join(dirname, 'empty')

    # Get the names of all the files in the template directory
    for file in os.listdir(_empty_dir):
        _empties_name.append(file)
        
    # Get a unique set of tags (code before the "_empty_" for matching input string)
    # Get a unique set of types (code after the "_empty_")
    # Get the extensions of the files
    temp_tags = []
    temp_types = []
    temp_exts = []
    for s in _empties_name:
        temp_tags.append(s[0:s.find(_sentinal)])
        temp_types.append(s[len(s)-6:len(s)-3])
        temp_exts.append(s[len(s)-3:len(s)])
        
    _tags = set(temp_tags)
    _types = set(temp_types)
    _extensions = set(temp_exts)
    
    #get the user input
    _layer = input("Layer name: ")
    _layer = _layer + "."

    #check that the name satisfies the template by checking tag and type
    #save the tag and type for use later when copying file
    c_tag = ""
    c_type = ""
        # check the tag
    for tag in _tags:
        i = _layer.find(tag)
        if i == 0:
            c_tag = tag
            break
        # If tag wasnt correct, exit
    if i < 0:
        input("incorrect tag, copy failed... exiting")
        exit(1)
        #check the type
    for ty in _types:
        j = _layer.find(ty)
        if j > 0:
            c_type = ty
            break
        # If type wasnt found, exit
    if j < 0:
        input("incorrect type, copy failed... exiting")
        exit(1)

    # Since all is good proceed with copying the .dbf, .prj, .shp and .shx
    for ex in _extensions:
        shutil.copyfile(os.path.join(_empty_dir, '{}_empty{}{}'.format(c_tag, c_type, ex)), os.path.join(dirname, '{}{}'.format(_layer, ex)))
    

if __name__ == "__main__":
    main()
