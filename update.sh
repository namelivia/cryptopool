#!/bin/bash
python2.7 scrappers/scrapperLaLigaOficial.py
sh ./data/reloadData.sh >> /tmp/cryptoporraLog
cat /tmp/cryptoporraLog | mail -s "Cryptoporra update" ohcan2@gmail.com
exit 0

