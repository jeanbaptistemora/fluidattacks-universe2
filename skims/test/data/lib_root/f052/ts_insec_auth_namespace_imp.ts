import * as CryptoJSAlias from 'crypto-js';

const key: string = "AnyKey";
const message: string = "SensibleData";

// Line 7 must be marked.
const hmacSHA1: CryptoJSAlias.lib.WordArray = CryptoJS.HmacSHA1(message, key);

// Line 10 must be marked.
const hmacSHA256: CryptoJSAlias.lib.WordArray = CryptoJS.HmacSHA256(message, key);
