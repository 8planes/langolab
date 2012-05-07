var MONGO_DB = "db";

module.exports = {
    COOKIE_SECRET: process.env.COOKIE_SECRET || "keyboard cattt",
    SESSION_SECRET: process.env.SESSION_SECRET || "keyboard kitteh",
    MONGO_DB: MONGO_DB,
    MONGO_DB_URL: process.env.MONGO_DB || "mongodb://localhost/" + MONGO_DB,
    REDIS_URL: process.env.REDISTOGO_URL || "redis://localhost:6379",
    FACEBOOK_APP_ID: process.env.FACEBOOK_APP_ID || '160435570643887',
    FACEBOOK_APP_SECRET: process.env.FACEBOOK_SECRET_KEY || 
        '396acfb54060bcfaa70d941d275b16c0',
    BASE_URL: process.env.BASE_URL || 'http://localhost:8000',
    OPENTOK_API_KEY: '14933842',
    OPENTOK_API_SECRET: '4d3a45becd34ab8f9fb2156ab1732bbe4ce1e16a'
};
