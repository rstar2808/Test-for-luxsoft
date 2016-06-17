function(doc) {
    if ((doc.type == "tax") && (doc.is_active)){
        emit(doc.name, doc.proc);
    }
}