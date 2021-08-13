using System;
class jwtbuild {

   public static void Main() {

      var decodedtoken1 = decoder.Decode(token, secret, verify: false);
      var json_deco = decoder.Decode(token, secret, verify: true);

      var decodedtoken2 = new JwtBuilder()
         .MustVerifySignature()
         .WithSecret(secret)
         .Decode(forgedtoken1);


      var decodedtoken2 = new JwtBuilder()
         .WithSecret(secret)
         .Decode(forgedtoken1);

      var json = JwtBuilder.Create()
         .WithAlgorithm(new HMACSHA256Algorithm())
         .WithSecret(secret)
         .MustVerifySignature()
         .Decode(token);

      var json2 = JwtBuilder.Create()
         .WithAlgorithm()
         .WithSecret(secret)
         .Decode(token);

      var json3 = JwtBuilder.Create();

   }
}
