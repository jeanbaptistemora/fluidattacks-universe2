CryptoJS.enc.Base64.parse(source);

CryptoJS.enc.Base64.parse("secret");
CryptoJS.enc.Utf16.parse('secret');
CryptoJS.enc.Utf16LE.parse(`source`);
CryptoJS.enc.Hex.parse("sec\"ret");
CryptoJS.enc.Latin1.parse('sec\'ret');
CryptoJS.enc.Utf8.parse(`sec\`ret`);
