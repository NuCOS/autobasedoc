# -*- coding: utf-8 -*-
"""
post processing all test-xml for jenkins
"""
import sys, os

if not len(sys.argv) == 3:
    raise Exception("give me 2 arguments")

filename = sys.argv[1]
py = sys.argv[2]

if not os.path.exists(filename):
    raise Exception("file not found")

raw_fn = filename.split(".")[0]

f = open(filename, "r")
txt = f.read()
f.close()

f = open("".join([raw_fn,"_",py,".xml"]), "w")
txt = txt.replace("UTest", "".join(["UTest_",py,"_"]))
f.write(txt)
f.close

os.remove(filename)