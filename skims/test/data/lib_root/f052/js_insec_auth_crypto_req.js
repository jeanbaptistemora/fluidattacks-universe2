const crypto = require("crypto");

const secret = "GfG";

// Both following lines should be marked
const hash = crypto.createHmac("sha256", secret);
hash = crypto.createHmac("sha1", secret);

// Next following lines are safe:
const hash1 = crypto.createHmac("sha512", secret);
hash1 = crypto.otherMethod("sha1", secret);
hash1 = cryptoSafe.createHmac("sha1", secret);
