using System;
class jwtbuild {

   public static void Main() {

      var insecure_decode = decoder.Decode(token, secret, verify: false);

      var secure_decode = decoder.Decode(token, secret, verify: true);

      var insecure_decode2 = decoder.Decode(token, secret, false);

      var secure_decode2 = decoder.Decode(token, secret, true);

   }
}
