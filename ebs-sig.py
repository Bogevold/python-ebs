#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, gnupg, ConfigParser, shutil
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


cfg = ConfigParser.ConfigParser()
cfg.read('/u01/app/apps/apps_st/appl/xxsi/12.0.0/bin/ebs-sig.ini')

#stiFra = "/u01/sepa/ut"
stiFra = cfg.get('FILPLASSERINGER', 'stiFra')
#stiTil = "/u01/sg/"
stiTil = cfg.get('FILPLASSERINGER', 'stiTil')
#mappingFil = "/u01/app/apps/apps_st/appl/xxsi/12.0.0/bin/sepa_mapping.txt"
mappingFil = cfg.get('FILPLASSERINGER', 'mappingFil')
#NokkelHome = '/u01/si21a/sepa_nokler'
NokkelHome = cfg.get('FILPLASSERINGER', 'NokkelHome')
nklPwd = cfg.get('ANNET', 'NokkelPwd')

MILJO = cfg.get('MODI', 'Miljo')

gpg = gnupg.GPG(gnupghome=NokkelHome)
gpg.encoding = 'utf-8'
mappingTabell = {}

with open(mappingFil,"r") as f:
  for line in f:
    r = line.split()
    # print r
    if len(r) < 3 or r[0][0] == "#":
      continue
    r2 = [r[1], ' '.join(r[2:])]
    mappingTabell[r[0]] = r2

# print mappingTabell

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
        signDta = gpg.sign_file(stream, passphrase='Sommer2016')
        #print str(signDta)
        stream.close()
        utFil = stiTil + MILJO + "." + mappingTabell[org][0] + ".002.P001." + request + ".xml"
        fUt = open(utFil, "w")
        fUt.write(str(signDta))
        fUt.close()
        tattFilnavn = os.path.join(root, 'tatt', file)
        #print tattSti
        shutil.move(fulltFilnavn, tattFilnavn)

