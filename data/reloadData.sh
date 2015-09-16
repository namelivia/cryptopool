#!/bin/bash
echo "=====[RELOADING DATA]====="
echo "=====[Clearing the database]====="
mongo localhost:3001/meteor --eval "db.teams.remove({})"
mongo localhost:3001/meteor --eval "db.matches.remove({})"
echo "=====[Seeding the database]====="
mongoimport --host localhost:3001 --jsonArray --db meteor --collection teams teams.json
mongoimport --host localhost:3001 --jsonArray --db meteor --collection matches matches.json;
echo "=====[Fixing the database]====="
mongo localhost:3001/meteor ../.mongoscripts/fix_match_times.js
echo "=====[DONE]====="
