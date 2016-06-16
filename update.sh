#!/bin/bash
cd /root/cryptoporra
echo "=====[UPDATING DATA]====="
cd scrappers
python2.7 scrapperLaLigaOficial.py 5
#python2.7 scrapperLogos.py
#python2.7 scrapper20Minutos.py
cd ..
sh ./data/reloadData.sh >> /tmp/cryptoporraLog
#cat /tmp/cryptoporraLog | mail -s "Cryptoporra update" ohcan2@gmail.com
exit 0

