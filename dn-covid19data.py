#!/usr/bin/python3
# Bokwon Yoon
# requirement: Linux or WSL on windows (Mac - needs to change some command options)
#              poppler-utils preinstalled (ex. sudo apt-get install poppler-utils 

import os
from os import path
import re

cmd  = 'curl "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports/" -s '
cmd += "| sed -n '/Situation report/p' | sed 's@<a@\\n<a@g' | sed -r -n 's@.+\\\"(\/docs\/[^\\\"]+)\\\".+@\\1@p'"
cmd += ' > tmp.txt'
#print(cmd)
os.system(cmd)

with open('tmp.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    url = 'https://www.who.int'+line.rstrip()
    res = re.search('sitrep-[0-9]+', line)
    num = int(res.group().replace('sitrep-', ''))
    pdffile = 'sitrep-{:03d}.pdf'.format(num)
    txtfile = 'sitrep-{:03d}.txt'.format(num)

    if path.exists(pdffile):
        print('{} already exists.'.format(pdffile))
    else:
        cmd = 'wget -O ' + pdffile + ' -4 "{}" -q'.format(url)
        print(pdffile)
        os.system(cmd)

    if not path.exists(txtfile):
        cmd = 'pdftotext -layout {} {}'.format(pdffile, txtfile)
        print(cmd)
        os.system(cmd)



