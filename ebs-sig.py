#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, gnupg, ConfigParser, shutil
#
# Dokumentasjon for gunpg 
# https://pythonhosted.org/python-gnupg/#signing
# 

# Sette opp konfigurasjons håndterer
cfg = ConfigParser.ConfigParser()
cfg.read('/u01/app/apps/apps_st/appl/xxsi/12.0.0/bin/ebs-sig.ini')

#stiFra -> Rotkatalog for filer klare til signering
stiFra = cfg.get('FILPLASSERINGER', 'stiFra')
#stiTil -> Rotkatalog for signerte filer
stiTil = cfg.get('FILPLASSERINGER', 'stiTil')
#mappingFil -> Absolutt sti til fil som med mapping mellom distrikt og orgnr
mappingFil = cfg.get('FILPLASSERINGER', 'mappingFil')
#NokkelHome -> Hvor nøkler genert av gpg befinner seg
NokkelHome = cfg.get('FILPLASSERINGER', 'NokkelHome')
#nklPwd -> Passordet til privat nøkkel
nklPwd = cfg.get('ANNET', 'NokkelPwd')

# MILJO - Indikerer produksjon (P) eller testmiljø (T)
MILJO = cfg.get('MODI', 'Miljo')

# Initierer gnupg
gpg = gnupg.GPG(gnupghome=NokkelHome)
gpg.encoding = 'utf-8'
mappingTabell = {}


# Leser mappingfil til en dictionary for bruk i utsti
with open(mappingFil,"r") as f:
  for line in f:
    r = line.split()
    if len(r) < 3 or r[0][0] == "#":
      continue
    r2 = [r[1], ' '.join(r[2:])]
    mappingTabell[r[0]] = r2

# Traverserer "fraSti" og leter etter filer klare til signering
for root, dirs, files in os.walk(stiFra):
  for file in files:
    if file.endswith(".xml"):
      fulltFilnavn = os.path.join(root, file)
      org = file[:2]
      request = file[2:-4]      
      stiArr = root.split('/')
      nivaa = len(stiArr)
      # Tar kun filer i ett nivå under rotkatalogen 
      if nivaa == 5:
        stream = open(fulltFilnavn, "rb")
        signDta = gpg.sign_file(stream, passphrase='Sommer2016')
        stream.close()
        utFil = stiTil + MILJO + "." + mappingTabell[org][0] + ".002.P001." + request + ".xml"
        fUt = open(utFil, "w")
        fUt.write(str(signDta))
        fUt.close()
        # Flytter behandlet fil til "tattkatalog"
        tattFilnavn = os.path.join(root, 'tatt', file)
        shutil.move(fulltFilnavn, tattFilnavn)

