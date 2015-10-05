#!/bin/bash
EXEC_PATH="`dirname \"$0\"`"
echo "=====[Fixing the database]====="
mongo localhost:3001/meteor "$EXEC_PATH"/../.mongoscripts/fix_match_times.js
echo "=====[Creating indexes]====="
mongo localhost:3001/meteor --eval "db.matches.createIndex({ date : 1 })"
echo "=====[DONE]====="
