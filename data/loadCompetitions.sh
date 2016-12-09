#!/bin/bash
EXEC_PATH="`dirname \"$0\"`"
echo "=====[RELOADING COMPETITIONS]====="
echo "=====[Clearing the competitions]====="
mongo localhost:3001/meteor --eval "db.competitions.remove({})"
echo "=====[Loading the competitions]====="
mongoimport --host localhost:3001 --jsonArray --db meteor --collection competitions "$EXEC_PATH"/competitions.json
echo "=====[DONE]====="
