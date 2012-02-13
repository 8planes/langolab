exports.utcDate = function(date) {
    return new Date(date.getUTCFullYear(), 
                    date.getUTCMonth(), 
                    date.getUTCDate());
};
