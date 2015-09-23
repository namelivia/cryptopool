#!/bin/bash
EXEC_PATH="`dirname \"$0\"`"
echo "=====[RELOADING DATA]====="
echo "=====[Clearing the database]====="
mongo localhost:3001/meteor --eval "db.teams.remove({})"
mongo localhost:3001/meteor --eval "db.matches.remove({})"
echo "=====[Seeding the database]====="
mongoimport --host localhost:3001 --jsonArray --db meteor --collection teams "$EXEC_PATH"/teams.json
mongoimport --host localhost:3001 --jsonArray --db meteor --collection matches "$EXEC_PATH"/matches.json;
echo "=====[Fixing the database]====="
mongo localhost:3001/meteor "$EXEC_PATH"/../.mongoscripts/fix_match_times.js
echo "=====[Creating indexes]====="
mongo localhost:3001/meteor --eval "db.matches.createIndex({ date : 1 })"
mongo localhost:3001/meteor --eval "db.teams.createIndex({ id : 1 })"
echo "=====[DONE]====="
