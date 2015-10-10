#!/bin/bash
echo "=====[RELOADING DATA]====="
echo "=====[Clearing the database]====="
mongo localhost:3001/meteor --eval "db.teams.remove({})"
mongo localhost:3001/meteor --eval "db.matches.remove({})"
python2.7 scrappers/scrapperLaLigaOficial.py
sh ./data/reloadData.sh >> /tmp/cryptoporraLog
cat /tmp/cryptoporraLog | mail -s "Cryptoporra update" ohcan2@gmail.com
exit 0

