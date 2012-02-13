var MONGO_DB = "db";

module.exports = {
    COOKIE_SECRET: process.env.COOKIE_SECRET || "keyboard cattt",
    SESSION_SECRET: process.env.SESSION_SECRET || "keyboard kitteh",
    MONGO_DB: MONGO_DB,
    MONGO_DB_URL: process.env.MONGO_DB || "mongodb://localhost/" + MONGO_DB
};
