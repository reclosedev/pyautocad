#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import re
import csv
import os

from pyautocad import Autocad
from pyautocad.utils import mtext_to_string

known_targets_file = "cables_kommash_zag_known.csv"
output_file = "cables_kommash_zag.csv"

def get_known_targets():
    if not os.path.exists(known_targets_file):
        print "Can't find file with known targets:", known_targets_file
        return dict()
        
    targets = dict()
    
    reader = csv.reader(open(known_targets_file, "r"), delimiter=';')
    for row in reader:
        if len(row) < 3:
            continue
        row = [x.decode('windows-1251') for x in row]
        targets[row[0]] = row[2]
        #print row[0]
    return targets

def get_cables():
    targets = get_known_targets()
    for text in iter_objects_fast("dbmtext"):
        text = ias(text, ACAD.IAcadMText)
        name = source = target = None
        cable = section = length = ""
        text = text.TextString
#        if u"П1-ШУ" in text:
#            print "!!!!!!!!!!!", text
           
        text = unformat_text(text)
        print text    
        #m_cable = re.match(ur"(.*?)-(.*?)\s*\\P\s*(.*?)-([\dxх,\(\)]+)\s+(\d+)\s*[мm]", text)
        m_cable = re.match(ur"(?P<cable>.*?)-(?P<section>[\dxх,\(\)]+)\s+(?P<length>\d+)\s*[мm]\\P\s*(?P<name>[^-]+)-(?P<source>.+)\s*", text)
        if not m_cable:
            m_cable = re.match(ur"(?P<name>.*?)-(?P<source>.*?)\s*\\P\s*(?P<cable>.*?)-(?P<section>[\dxх,\(\)]+)\s+(?P<length>\d+)\s*[мm]", text)
            if not m_cable:
                continue
        # TODO remove this
        names = ['name', 'source', 'cable', 'section', 'length']
        name, source, cable, section, length = [m_cable.group(grp) for grp in names]
      
        print "!!!", text, '\n'
        
        cable_name = "%s-%s" % (name, source)
        target = targets.get(cable_name)
        
        if not target:
            target = get_target(name, source, cable, section, length)
            
        yield (cable_name, source, target, cable, section, length)

def get_target(name, source, cable, section, length):
    return name
    #extra logic
    m = r(ur"(.*?)(\d+)", name)
    if not m:
        return "" 
    lcode, lnum = m
    
    m = r(ur"(.*?)(\d+)", source)
    scode = snum = None
    if not m:
        scode = source
        snum = None
    else:
        scode, snum = m
    
    if u"ШМА" in scode:
        if snum == "1":
            table = {1:1, 2:3, 3:5, 4:7}
        elif snum == "2":
            table = {1:2, 2:4, 3:6, 4:8}
        elif snum == "3":
            table = {1:9, 2:10, 3:11, 4:12, 5:13}
        n = table.get(int(lnum))
        if n:
            return "ШУ%s" % n
            
    if u"ШУ" in scode:
        return "ШРА%s" % snum
    if u"QS" in scode:
        return "ШТМ%s" % (int(snum) - 1) 
    if u"ШРА" in scode and u"95" in section and u"П" == lcode:
        return "ЩСТ%s.%s" % (snum, lnum)
    if u"ЩРО" in scode:
        return "ЩОхх"
    return ""
    
def r(exp, str):
    m = re.match(exp, str)
    if m:
        return m.groups()
    return None
    

def main():
    output = open(output_file, "w")
    sorted_cables = sorted(get_cables(), key=lambda x: (x[1], x[0]))
    for line in sorted_cables:
        output.write("%s\n" % ";".join(line).encode("windows-1251"))
            
if __name__ == "__main__":
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    elif len(sys.argv) == 3:
        known_targets_file = sys.argv[2]
        
    begin_time = time.time()
    main()
    print "Elapsed: %.4f" % (time.time() - begin_time)      
        

