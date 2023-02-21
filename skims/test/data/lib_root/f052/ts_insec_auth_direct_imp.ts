import hmacSHA1 from 'crypto-js/hmac-sha1';
import hmacSHA256 from 'crypto-js/hmac-sha256';

const key: string = "AnyKey";
const message: string = "SensibleData";

// Lines 8 and 9 should be marked
const hmacSHA1Result: CryptoJS.lib.WordArray = hmacSHA1(message, key);
const hmacSHA256Result: CryptoJS.lib.WordArray = hmacSHA256(message, key);
