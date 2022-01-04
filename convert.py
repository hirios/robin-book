from os import listdir, rename
from os.path import isfile, join
import subprocess
import platform
import os


# return name of file to be kept after conversion.
# we are just changing the extension. azw3 here.
def get_final_filename(f):
    f = f.split(".")
    filename = ".".join(f[0:-1])
    processed_file_name = filename+".mobi"
    return processed_file_name


# return file extension. pdf or epub or mobi
def get_file_extension(f):
    return f.split(".")[-1]


# list of extensions that needs to be ignored.
ignored_extensions = ["pdf", "mobi", "epub"]

# here all the downloaded files are kept
mypath = "EPUB/"

# path where converted files are stored
mypath_converted = "AZW3/"

# path where processed files will be moved to, clearing the downloaded folder
mypath_processed = "ignore/"

raw_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
converted_files =  [f for f in listdir(mypath_converted) if isfile(join(mypath_converted, f))]

if '.gitignore' in raw_files:
    raw_files.remove('.gitignore')

if '.gitignore' in converted_files:
    converted_files.remove('.gitignore')

ebook_convert_path = "ebook-convert"
if platform.system() == "Linux":
    if os.system("hash ebook-convert > /dev/null 2>&1") != 0:
        ebook_convert_path = "/app/calibre-bin/calibre/ebook-convert"
    

for f in raw_files:
    final_file_name = get_final_filename(f)
    extension = get_file_extension(f)
    if final_file_name not in converted_files and extension not in ignored_extensions:
        print("Converting : " + f)
        try:
            subprocess.call([ebook_convert_path, mypath+f, mypath_converted + final_file_name]) 
            s = rename(mypath+f, mypath_processed+f)
            print(s)
        except Exception as e:
            print(e)
    else:
        print("Already exists : " + final_file_name)
