#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
#Her havner produserte  filer /u01/sepa/ut/{SI – 01 -02 osv}
#De som er tatt /u01/sepa/ut/{SI – 01 -02 osv}/tatt
#Signeres til /u01/sg

stiFra = "/u01/sepa/ut"
stiTil = "/u01/sg"

for root, dirs, files in os.walk(stiFra):
  for file in files:
    if file.endswith(".xml"):
      #print(os.path.join(root, file))
      stiArr = root.split('/')
      nivaa = len(stiArr)
      if nivaa == 5:
        print "Fra område: {0}".format(root)
        print "Filenavn:   {0}".format(file)
