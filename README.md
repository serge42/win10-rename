# Rename.py

A simple command line script using python 3.7 to rename multiple files at once using regular expressions as Windows 10 does not ship with any such basic utility :(.  It is mostly a copy of the rename command available on MacOs 15 Mojave.

## Usage

```python rename.py [renamings, flags] <files-selection>```

When multiple replacement are given, they are applied one after another. 

### Options

```-n: ``` dry-run; shows a list of modification the given operation would perform.  

```-z: ``` normalize filenames: replaces white-space characters (\s) by underscores (_) and removes all characters that are not either alphanumeric, dot (.), dash (-), plus (+), comma (,), semicolon (;) or brackets ([]).

```-e <matching-regexp> <replacement-string>: ``` replaces filenames matched by the regexp by the given replacement. Groups are supported and can be used in the replacement string as '\1', '\2', etc. following Python's 're' specification. 

```-S <substring> <replacement-string>: ``` Replaces all instances of a substring of filenames by another substring. Usefull to avoid escaping special regexp characters.

```-s <substring> <replacement-string>: ``` Same as '-S' but only replaces the first instance of the substring.  


## Examples

Replacing all dots (.) in filenames except the final one delimiting the extension for all '.ext' files in the current directory:  
```rename.py -e "\." "_" -e "_(\w{3})" ".\1" *.ext```

## Limitations
For now, it is not possible to group flag arguments. E.g. rename.py -nze \<arg1\> \<arg2\> does not work; use rename.py -n -z -e \<arg1\> \<arg2\> instead.

This may be improved in the future, if I find it to be too much of an annoyance.
