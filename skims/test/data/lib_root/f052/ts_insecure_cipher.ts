import crypto from 'crypto';

function unsafe_encrypt(password:string, algorithm: string = 'aes-256-cbc'): string {
    var cipher = crypto.createCipher(algorithm, password);
    return cipher;
}

function unsafe_decrypt(password:string): string {
    const algo:string = 'rc4'
    var decipher = crypto.createDecipher(algo, password);
    return decipher;
}


function safe_decrypt(password:string): string {
    const algo:string = 'ecdsa-aria-128-gcm'
    var decipher = crypto.createDecipher(algo, password);
    return decipher;
}
