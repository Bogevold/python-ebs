#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, gnupg
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


# Testkode signering
gpg = gnupg.GPG(gnupghome='/u01')
gpg.encoding = 'utf-8'
input_data = gpg.gen_key_input(key_type="RSA", key_length=1024)
key = gpg.gen_key(input_data)
stream = open('/u01/sepa/ut/SI/SI12345.xml', "rb")
signed_data = gpg.sign_file(stream)
f = open("/u01/test.xml.pgp", "w")
f.write(str(signed_data))
f.close()

# www https://pythonhosted.org/python-gnupg/#signing
