#!/bin/bash
cd /root/cryptoporra
echo "=====[CLEANING USER DDATA]====="
mongo localhost:3001/meteor --eval "db.messsages.remove({})"
mongo localhost:3001/meteor --eval "db.pools.remove({})"
mongo localhost:3001/meteor --eval "db.notifications.remove({})"
mongo localhost:3001/meteor --eval "db.users.remove({})"
mongo localhost:3001/meteor --eval "db.matches.remove({})"
