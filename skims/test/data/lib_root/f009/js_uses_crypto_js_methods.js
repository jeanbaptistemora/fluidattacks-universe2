import * as CryptoJS from "crypto-js";

function hasCrytoJsFunctions(arg) {

  //Unsafe
  const Utf16LE = CryptoJS.enc.Utf16LE.parse("a23ijl");
  const Latin1 = CryptoJS.enc.Latin1.parse("sec\"ret");
  const utf8 = CryptoJS.enc.Utf8.parse("Fmljho");

  // Safe values
  const initDate = format(parse("hello"));
  const base64 = CryptoJS.enc.base64.parse(arg);
}
