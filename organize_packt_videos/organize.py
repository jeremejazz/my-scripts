#!/usr/bin/env python

"""

======================================================================
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
======================================================================

Usage: 

This script is used for organizing Packtpub downloaded course into directories containing titles especially those purchased from Humblebundle.

Requirements: 

python3 

Instructions: 

* Copy the contents of index to `toc.txt`. It is usually contained in a docx file. 
* Move this script to the same directory where the video files and toc.txt are located. 
* Run this code. A videos folder should be created along with subdirectories containing section titles and video subsection titles. 


"""
import os
import shutil
import re


def create_index():
    index = {}
    section_pattern = r"Section (\d*):\s(\D*)"
    subsection_pattern = r"^(\d*)\.(\d*)(.*)"
    with open("toc.txt") as f:
        lines = f.readlines()
        for line in lines:
            ## match subsection 
            s_matches = re.findall(section_pattern, line)
            if(s_matches):
                index[s_matches[0][0]] = {}
                index[s_matches[0][0]]['title'] = s_matches[0][1].strip()
            
            ss_matches = re.findall(subsection_pattern, line)
            if (ss_matches):
                section = ss_matches[0][0]
                subsection = ss_matches[0][1]
                text = ss_matches[0][2]
                index[section][subsection] = text
    
    return index

def filter_text(text):
    new_text = re.sub(r"[\"\?\.]+", "", text, flags=re.IGNORECASE)
    return new_text


def main():
        
    index = create_index()

    if not os.path.exists("videos"): 
        os.mkdir("videos")


    regex = r"^video(\d*)_(\d*).mp4"
    for idx, filename in enumerate(sorted(os.listdir(os.getcwd()))):

        matches = re.finditer(regex, filename)
        if(matches):
            for match in matches:

                section = match.group(1)
                subsection = match.group(2)
                title = index[section]['title']
                subsection_title = filter_text(index[section][subsection])
                if not os.path.exists(os.path.join('videos', f"{section} - {title}")):
                    os.mkdir(os.path.join('videos', f"{section} - {title}"))
                
                shutil.move(filename, os.path.join('videos', f"{section} - {title}", f"{section}.{subsection} - {subsection_title}.mp4"))
if __name__ == "__main__":
    main()


