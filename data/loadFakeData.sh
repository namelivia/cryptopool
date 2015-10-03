#!/bin/bash
EXEC_PATH="`dirname \"$0\"`"
echo "=====[RELOADING FAKE DATA]====="
echo "=====[Clearing the database]====="
mongo localhost:3001/meteor --eval "db.users.remove({})"
mongo localhost:3001/meteor --eval "db.pools.remove({})"
echo "=====[Seeding the database]====="
mongoimport --host localhost:3001 --jsonArray --db meteor --collection users "$EXEC_PATH"/users.json
mongoimport --host localhost:3001 --jsonArray --db meteor --collection pools "$EXEC_PATH"/pools.json
echo "=====[Fixing the database]====="
echo "=====[Creating indexes]====="
echo "=====[DONE]====="
