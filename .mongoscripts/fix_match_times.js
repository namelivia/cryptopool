var cursor = db.matches.find()
while (cursor.hasNext()) {
	var doc = cursor.next();
	db.matches.update({_id : doc._id}, {$set : {date : new Date(doc.date)}})
}
