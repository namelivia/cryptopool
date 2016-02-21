#!/bin/bash
cd /root/cryptoporra
echo "=====[RELOADING DATA]====="
echo "=====[Clearing the database]====="
mongo localhost:3001/meteor --eval "db.teams.remove({})"
mongo localhost:3001/meteor --eval "db.matches.remove({})"
mongo localhost:3001/meteor --eval "db.players.remove({})"
python2.7 scrappers/scrapperLaLigaOficial.py
python2.7 scrappers/scrapperLogos.py
python2.7 scrappers/scrapper20Minutos.py
sh ./data/reloadData.sh >> /tmp/cryptoporraLog
#cat /tmp/cryptoporraLog | mail -s "Cryptoporra update" ohcan2@gmail.com
exit 0

