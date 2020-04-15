#!/usr/bin/env python
import re, os, sys
import glob
from sys import argv

dry_run=False

def main():
    global dry_run

    # Getting list of files to be renamed
    file_match = argv[-1]
    # print(file_match)
    ptn = re.sub(r'([\[\]])','[\\1]', file_match)
    files = glob.glob(ptn)
    if len(files) <= 0:
        print('No files matched, exiting')
        sys.exit(0)
    files = remove_crnt_dir(files)
    path, filenames = split_dirname(files)
    # print(path)
    # print(filenames)

    # Loop on modifications
    renamed = filenames.copy()
    i=0
    while i < len(argv) - 1: # last arg is file-match
        arg = argv[i]
        if arg == '-n':
            dry_run = True
        elif arg == '-z':
            renamed = normalize(renamed)
        elif arg == '-e':
            match_regexp=argv[i+1]
            replacement = argv[i+2]
            i+=2
            renamed = regexp(renamed, match_regexp, replacement)
        elif arg == '-S' or arg == '-s':
            substr = argv[i+1]
            replacement = argv[i+2]
            i+=2
            c = 0 if arg == '-S' else 1
            renamed = replace_all(renamed, substr, replacement, count=c)
        
        i+=1

    if len(path) > 0: # reattach path
        for i,f in enumerate(renamed):
            renamed[i] = path + '\\' + f

    if dry_run:
        dry_run_print(files, renamed)
    else:
        apply_rename(files, renamed)
    
def regexp(files, match_regexp, replacement, count=0):
    # print('MATCH_REGEXP: {}'.format(match_regexp))
    p = re.compile(match_regexp)
    new_files = []
    for f in files:
        new_f = p.sub(replacement, f)
        new_files.append(new_f)
    return new_files

def normalize(files):
    '''
    Accepted chars:
    Windows: anything except ASCII's control characters and \/:*?"<>|
    Linux, OS-X: anything except null or /
    '(' ')' ',' are not accepted as they are used in shell commands'''
    files = regexp(files, r'\s', '_')
    files = regexp(files, r'[^\w\[\]\.\+-;]', '') # Remove non-alphanumeric characters, except: [] . - + ;
    return files

def replace_all(files, substr, replacement, count=0):
    substr = re.escape(substr)
    return regexp(files, substr, replacement, count=count)
    # p = re.compile(substr)
    # new_files = []
    # for f in files:
    #     new_f = p.sub(replacement, f, count=count)
    #     new_files.append(new_f)
    # return new_files

def dry_run_print(files, renamed):
    assert len(files) == len(renamed)
    for i in range(len(files)):
        print('{} => {}'.format(files[i], renamed[i]))

def apply_rename(files, renamed):
    # raise NotImplementedError('not working yet')
    for i in range(len(files)):
        os.rename(files[i], renamed[i])

def split_dirname(files):
    path = None
    filenames = []
    for f in files:
        parts = f.split('\\')
        if len(parts) == 1:
            return '', files # No parent dir
        if path:
            assert path == '\\'.join(parts[0:-1]), "Can't process multiple files from distinct paths"
        else:
            path = '\\'.join(parts[0:-1])
        filenames.append(parts[-1])

    return path, filenames

def remove_crnt_dir(files):
    '''Windows often refers to .\filename, remove the current dir from the filename'''
    p = re.compile('\\.\\\\')
    new_files = []
    for f in files:
        re.sub(r'\\', r'\\\\', f)
        if p.match(f):
            # print('STARTS WITH CRNT DIR')
            f = f[2:]
        # else:
        #     print(f)
        #     print(p.match(f))
        new_files.append(f)
    return new_files

def print_usage():
    print('Usage: rename.py [flags] file_match')
    print('\t-n: dry-run, does not rename')
    print('\t-z: normalize')
    print('\t-e <match regexp> <replacement regexp>. Use "\1", "\2", etc. to refer to matched groups')
    print('\t-S <substring> <replacement>: replace all occurences')
    print('\t-s <substring> <replacement>: replace first occurence')

if __name__ == "__main__":
    if len(argv) < 2:
        print_usage()
        sys.exit(0)

    main()