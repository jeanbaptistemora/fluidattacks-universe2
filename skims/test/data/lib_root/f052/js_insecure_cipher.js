function insecureModes() {
    var encrypted = CryptoJS.AES.encrypt("Message", "Secret Passphrase", {
        mode: CryptoJS.mode.CFB, // Insecure
        padding: CryptoJS.pad.AnsiX923
    });

    var crypto = CryptoJS.mode.OFB
    var encrypted_mess = CryptoJS.AES.encrypt("Message", "Secret Passphrase", {
        mode: crypto, // Insecure
        padding: CryptoJS.pad.AnsiX923
    });

    var miss_encrypt = CryptoJS.AES.encrypt("Message", "Secret Passphrase", {
        padding: CryptoJS.pad.AnsiX923
    });
}
