import * as CryptoJS from 'crypto-js';

export class EncryptionService {
  constructor() {}

	unsafe1(plainText: string, key: string) {
    const encrypted = CryptoJS.RC4.encrypt(plainText, key, {
      mode: CryptoJS.mode.ECB,
    });
    return encrypted.ciphertext.toString(CryptoJS.enc.Base64);
  }

  unsafe2(plainText: string, key: string) {
		const cipher_mode = CryptoJS.mode.CBC;
		const config = {mode: cipher_mode, padding: CryptoJS.pad.NoPadding};
    const encrypted = CryptoJS.AES.encrypt(plainText, key, config);
    return encrypted.ciphertext.toString(CryptoJS.enc.Base64);
  }

	safe(plainText: string, key: string) {
    const encrypted = CryptoJS.AES.encrypt(plainText, key, {
      mode: CryptoJS.mode.GCM,
    });
    return encrypted.ciphertext.toString(CryptoJS.enc.Base64);
  }

}
