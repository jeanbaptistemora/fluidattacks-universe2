#!/usr/bin/python
import sys
import os
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
import stat

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)
    os.chmod(file_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

for d in sys.path:
    full_path = d + '/social_core/backends/azuread.py'
    if os.path.exists(full_path):
        replace(full_path, "return response.get('upn')",
                "return response.get('email') \
if response.get('upn') is None else response.get('upn')")
        replace(full_path, "'email': response.get('upn'),",
                "'email': response.get('email') if response.get('upn') \
is None else response.get('upn'),")


