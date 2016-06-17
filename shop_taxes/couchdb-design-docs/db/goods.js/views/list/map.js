function(doc) {
    if ((doc.type == "product") && (doc.is_active)){
        emit(doc.name, doc.cost);
    }
}