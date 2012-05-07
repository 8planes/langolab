exports.utcDate = function(date) {
    return new Date(Date.UTC(date.getUTCFullYear(), 
                             date.getUTCMonth(), 
                             date.getUTCDate()));
};
