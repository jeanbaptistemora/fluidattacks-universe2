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

function secureMode() {
    var safe_mode = CryptoJS.mode.CTR
    var message = CryptoJS.AES.encrypt("Message", "passphrase", {
        mode: safe_mode,
        padding: CryptoJS.pad.AnsiX923
    });
}
