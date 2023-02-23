import *  as cryptoAlias from "crypto"

const secret = "GfG";

// Both following lines should be marked
let hash = cryptoAlias.createHmac("sha256", secret);
hash = cryptoAlias.createHmac("sha1", secret);

// Next following lines are safe:
var hash1 = cryptoAlias.createHmac("sha512", secret);
hash1 = cryptoAlias.otherMethod("sha1", secret);
hash1 = cryptoSafe.createHmac("sha1", secret);
