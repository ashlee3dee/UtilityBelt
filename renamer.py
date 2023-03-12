import os
import sys

path = str(sys.argv[1])
filetype = str(sys.argv[2])

for filename in os.listdir(path):
    prefix, num = filename[:-4].split('_')
    num = num.zfill(4)
    new_filename = prefix + "_" + num + filetype
    os.rename(os.path.join(path, filename), os.path.join(path, new_filename))
    #you could compile a list of valid filenames assuming that all files that start with "output_" and end with ".png" are valid files:

l = [(x, "output" + x[7:-4].zfill(4) + filetype) for x in os.listdir(path) if x.startswith("output_") and x.endswith(".png")]

for oldname, newname in l:
    os.rename(os.path.join(path,oldname), os.path.join(path,newname))
