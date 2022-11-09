import * as CryptoJS from "crypto-js";

function hasCrytoJsFunctions(arg) {
  const chartString = "Hello world";

  const chart2 = arg;
  const base64 = CryptoJS.enc.Base64.parse(chartString);
  const utf16 = CryptoJS.enc.Utf16.parse(chart2);
  const Utf16LE = CryptoJS.enc.Utf16LE.parse("a23ijl");
  const Hex = CryptoJS.enc.Hex.parse(chartString);
  const Latin1 = CryptoJS.enc.Latin1.parse("iuop8o");
  const utf8 = CryptoJS.enc.Utf8.parse("Fmljho");
}
