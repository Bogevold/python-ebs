#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, gnupg
#Her havner produserte  filer /u01/sepa/ut/{SI – 01 -02 osv}
#De som er tatt /u01/sepa/ut/{SI – 01 -02 osv}/tatt
#Signeres til /u01/sg
# Filformat:
#     P.00091062305.002.P001.1840737.xml
#
# Engangsoperasjoner for å generere nøkler
# input_data = gpg.gen_key_input(key_type="RSA", key_length=1024)
# key = gpg.gen_key(input_data)

# www https://pythonhosted.org/python-gnupg/#signing
# Sjekk installering remote (var en link til nedlasting nede i dokumentasjonen)




stiFra = "/u01/sepa/ut"
stiTil = "/u01/sg/"
gpg = gnupg.GPG(gnupghome='/u01')
gpg.encoding = 'utf-8'

for root, dirs, files in os.walk(stiFra):
  for file in files:
    if file.endswith(".xml"):
      fulltFilnavn = os.path.join(root, file)
      org = file[:2]
      request = file[2:-4]      
      stiArr = root.split('/')
      nivaa = len(stiArr)
      if nivaa == 5:
        stream = open(fulltFilnavn, "rb")
        signDta = gpg.sign_file(stream)
        stream.close()
        utFil = stiTil + org + "/P.00091062305.002.P001." + request + ".xml"
        fUt = open(utFil, "w")
        fUt.write(str(signDta))
        fUt.close()

