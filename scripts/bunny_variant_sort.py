#!/usr/bin/python

import os

VariantArraySplit = os.environ["Variant"].split(".")
BaseVariants = ["TegraP1Lin","TegraP1Integrity","TegraP1"]
SortedArray = []

if any(i in BaseVariants for i in VariantArraySplit):
    skipindex = 2
else:
    skipindex = 0

for word in sorted(VariantArraySplit[skipindex:]):
    SortedArray.append(word)

for i in range(0,skipindex):
    SortedArray.insert(i,VariantArraySplit[i])


os.environ["Variant"] = ".".join(SortedArray)



