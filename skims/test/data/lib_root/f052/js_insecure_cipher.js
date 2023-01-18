function insecureModes() {
    var unsafe_1 = CryptoJS.AES.encrypt("Message", "Secret Passphrase", {
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.AnsiX923
    });

    var crypto = CryptoJS.mode.ECB
    var unsafe_2 = CryptoJS.AES.encrypt("Message", "Secret Passphrase", {
        mode: crypto,
        padding: CryptoJS.pad.AnsiX923
    });

    var unsafe_3 = CryptoJS.AES.encrypt("Message", "Secret Passphrase", {
        padding: CryptoJS.pad.AnsiX923
    });
}

function secureMode() {
    var safe_mode = CryptoJS.mode.CTR
    var safe = CryptoJS.AES.encrypt("Message", "passphrase", {
        mode: safe_mode,
        padding: CryptoJS.pad.AnsiX923
    });

    var safe_2 = CryptoJS.AES.encrypt(
        JSON.stringify(data),
        rootScope.base64Key,
        {
            iv: rootScope.iv
        },
		{
            mode : CryptoJS.mode.CFB
        },
    );
}
