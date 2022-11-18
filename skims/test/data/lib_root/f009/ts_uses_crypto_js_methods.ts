import {enc} from "crypto-js";

function hasCrytoJsFunctions(arg: string) {

  // Danger values
  const base64 = enc.Base64.parse("danger_value");
  const Utf16 = enc.Utf16.parse("danger_value");
  const hex = enc.Hex.parse("danger_value");

  // Safe values
  const Latin1 = enc.Latin1.parse(arg);
}
