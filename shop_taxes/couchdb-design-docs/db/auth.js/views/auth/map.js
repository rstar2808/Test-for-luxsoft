function(doc) {
    if ((doc.type == "user") && (doc.is_active)) {
        emit(doc.username.toLowerCase(), doc.password);
    }
}