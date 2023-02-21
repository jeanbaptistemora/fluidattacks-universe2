import * as CryptoJSAlias from 'crypto-js';

const key: string = "AnyKey";
const message: string = "SensibleData";

// Line 7 must be marked.
const hmacSHA1: CryptoJSAlias.lib.WordArray = CryptoJSAlias.HmacSHA1(message, key);

// Line 10 must be marked.
const hmacSHA256: CryptoJSAlias.lib.WordArray = CryptoJSAlias.HmacSHA256(message, key);

//Safe lines: None of following lines should be marked:

const hmacSHA512: CryptoJSAlias.lib.WordArray = CryptoJSAlias.HmacSHA512(message, key);
const hmacSHA: CryptoJSAlias.lib.WordArray = CryptoJSAlias.Hmac(message, key);
