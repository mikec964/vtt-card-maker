#!/usr/bin/env python3
#
# https://drscotthawley.github.io/Resolving-OSX-Aliases/
# Resolve Mac OS X 'aliases' by finding where they point to
# Author: Scott H. Hawley
#
# Description:
# Mac OSX aliases are not symbolic links. Trying to read one will probably crash your code.
# Here a few routines to help. Run these to change the filename before trying to read a file.
# Intended to be called from within other python code
#
# Python port modified from https://hints.macworld.com/article.php?story=20021024064107356
#
# Requirements: osascript (AppleScript), platform, subprocess, shlex
#
# TODO: - could make it work in parallel when mutliple filenames are given
#
# NOTE: By default, this only returns the names of the original source files,
#       but if you set convert=True, it will also convert aliases to symbolic links.


import subprocess
import platform
import os


# returns true if a file is an OSX alias, false otherwise
def isAlias(path, already_checked_os=False):
    if (not already_checked_os) and ('Darwin' != platform.system()):  # already_checked just saves a few microseconds ;-)
        return False
    checkpath = os.path.abspath(path)       # osascript needs absolute paths
    # Next several lines are AppleScript
    line_1='tell application "Finder"'
    line_2='set theItem to (POSIX file "'+checkpath+'") as alias'
    line_3='if the kind of theItem is "alias" then'
    line_4='   return true'
    line_5='else'
    line_6='   return false'
    line_7='end if'
    line_8='end tell'
    cmd = "osascript -e '"+line_1+"' -e '"+line_2+"' -e '"+line_3+"' -e '"+line_4+"' -e '"+line_5+"' -e '"+line_6+"' -e '"+line_7+"' -e '"+line_8+"'"
    args = shlex.split(cmd)      # shlex splits cmd up appropriately so we can call subprocess.Popen with shell=False (better security)
    p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = p.wait()
    if (0 == retval):
        line = p.stdout.readlines()[0]
        line2 = line.decode('UTF-8').replace('\n','')
        if ('true' == line2):
            return True
        else:
            return False
    else:
        print('resolve_osx_alias: Error: subprocess returned non-zero exit code '+str(retval))
    return None


# returns the full path of the file "pointed to" by the alias
def resolve_osx_alias(path, already_checked_os=False, convert=False):        # single file/path name
    if (not already_checked_os) and ('Darwin' != platform.system()):  # already_checked just saves a few microseconds ;-)
        return path
    checkpath = os.path.abspath(path)       # osascript needs absolute paths
    # Next several lines are AppleScript
    line_1='tell application "Finder"'
    line_2='set theItem to (POSIX file "'+checkpath+'") as alias'
    line_3='if the kind of theItem is "alias" then'
    line_4='   get the posix path of (original item of theItem as text)'
    line_5='else'
    line_6='return "'+checkpath+'"'
    line_7 ='end if'
    line_8 ='end tell'
    cmd = "osascript -e '"+line_1+"' -e '"+line_2+"' -e '"+line_3+"' -e '"+line_4+"' -e '"+line_5+"' -e '"+line_6+"' -e '"+line_7+"' -e '"+line_8+"'"
    args = shlex.split(cmd)              # shlex splits cmd up appropriately so we can call subprocess.Popen with shell=False (better security)
    p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    retval = p.wait()
    if (0 == retval):
        line = p.stdout.readlines()[0]        
        source = line.decode('UTF-8').replace('\n','')
        if (convert):
            os.remove(checkpath)
            os.symlink(source, checkpath)
    else:
        print('resolve_osx_aliases: Error: subprocess returned non-zero exit code '+str(retval))
        source = ''
    return source


# used for multiple files at a time, just a looped call to resolve_osx_alias
def resolve_osx_aliases(filelist, convert=False):  # multiple files
    #print("filelist = ",filelist)
    if ('Darwin' != platform.system()):
        return filelist
    outlist = []
    for infile in filelist:
        source = resolve_osx_alias(infile, already_checked_os=True, convert=convert)
        if ('' != source):
            outlist.append(source)
    #print("outlist = ",outlist)
    return outlist


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Resolve OSX aliases')
    parser.add_argument('file', help="alias files to resolve", nargs='+')
    args = parser.parse_args()
    outlist = resolve_osx_aliases(args.file)
    print("outlist = ",outlist)

# NOTE: Currently this code only follows _one_ alias. If there’s an alias pointing to an alias to a file, it won’t resolve to that file. Full generality would involve adding an iterative or recursive way of traversing multiple aliases which…I may do later. ;-)
