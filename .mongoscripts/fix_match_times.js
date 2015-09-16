var cursor = db.matches.find()
	while (cursor.hasNext()) {
	var doc = cursor.next();
	var test = new Date(doc.date);
	db.matches.update({_id : doc._id}, {$set : {date : new Date(doc.date)}})
}
