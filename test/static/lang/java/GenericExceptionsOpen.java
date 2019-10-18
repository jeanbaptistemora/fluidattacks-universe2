import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import org.springframework.security.crypto.password.MessageDigestPasswordEncoder;

class GenericExceptionsOpen{
    public static void main(String args[]){
      try{
          int a[]=new int[7];
          a[4]=30/0;
          System.out.println("First print statement in try block");

          if (a[0] > 200) {
              // this comment should not comment the else if clause
              System.out.println("Big num");
          } else if (a[0] < (100)){
              System.out.println("Small num}");
          }

          if (a[0] > (200)) {System.out.println("Big num{");} else  if (a[0] < (100)){System.out.println("Small num");}

          if (a[0] > (200)) {System.out.println("Big num}");}
          else   if (a[0] < (100)){System.out.println("Small num}");}

          // this comment should not comment the entire file
          else {System.out.println("Not big not small num");}
      }

      MessageDigest messageDigest, messageDigest2;
      messageDigest = MessageDigest.getInstance("MD5");
      messageDigest.update(data.getBytes());
      byte[] messageDigestMD5 = messageDigest.digest();
      messageDigest2 = MessageDigest.getInstance("SHA-1");
      messageDigest2.update(data.getBytes());
      byte[] messageDigestSHA1 = messageDigest2.digest();

      Cipher des = Cipher // a comment
                  /*another comment*/          .getInstance(
               "DES/ECB/PKCS5Padding" // a comment
               /* A comment */
               "The provider as string");

      Cipher aes = Cipher // a comment
                  /*another comment*/          .getInstance(
               "AES/ECB/NoPadding" // a comment
               /* A comment */
               TheProviderAsAVar /* A comment */
               );

      Cipher aes = Cipher // a comment
                  /*another comment*/          .getInstance(
               "AES/ECB/PKcS5Pading" // a comment
               /* A comment */
               TheProviderAsAVar /* A comment */
               );

      Cipher aes = Cipher // a comment
                  /*another comment*/          .getInstance(
               "AES/CBC/PKCS5Padding" // a comment
               /* A comment */
               TheProviderAsAVar /* A comment */
               );

      Cipher rsa = Cipher // a comment
                  /*another comment*/          .getInstance(
               "RSA/EcB/OAEPWITHSHA-256ANDMGF1PADDING" // a comment
               /* A comment */
               TheProviderAsAVar /* A comment */
               );

      Cipher rsa = Cipher // a comment
                  /*another comment*/          .getInstance(
               "RSA/CBC/PkCS1Padding" // a comment
               /* A comment */
               TheProviderAsAVar /* A comment */
               );
      Cipher rsa = Cipher // a comment
                  /*another comment*/          .getInstance(
               "RSA" // a comment
               /* A comment */
               TheProviderAsAVar /* A comment */
               );

      SSLContext.getInstance( // a comment
               "SSL" // a comment
               /* A comment */);

        @RequestMapping(value = "*", // a comment
         method = {
             GET,
             PUT, // a comment
              DELETE})

        @RequestMapping(value = "*", // a comment
         method = {
             RequestMethod.PUT,  RequestMethod.POST ,  /* A comment */
               RequestMethod.POST})

      SSLContext.getInstance( // a comment
               "SsLv3" // a comment
               /* A comment */);

      des.init(Cipher.ENCRYPT_MODE, secretKeySpec);
      byte[] encrypted = des.doFinal(input.getBytes("UTF-8"));

      catch(NullException e){
         System.exit(1);
      }
      catch(ArithmeticException e){
         System.out.println("Warning: ArithmeticException");
      }
      catch(ArrayIndexOutOfBoundsException e){
         System.out.println("Warning: ArrayIndexOutOfBoundsException");
      }
      /* autogenerated - output block end */;
      catch(


            Exception e){
         System.out.println("Warning: Some Other exception");
      }
      catch(Exception e      ){
         log.info("The error was" + e);
      }
      catch   (NullPointerException|Exception e)   {
         log.info("The error was" + e);
      }
      catch   (java.io.IOException|Exception|ArithmeticException e)   {
         log.info("The error was" + e);
      }
      catch   (Exception|java.lang.ArithmeticException|RuntimeException)   {
         log.info("There was an error");
      }
      catch   (
            java.lang.ArithmeticException|java.io.IOException)   {
         log.info("There was an error");
      }
      catch   (java.lang.ArithmeticException|
            java.io.IOException e)   {
         log.info("There was an error");
      }
      catch(Exception e){
         System.out.println("Warning: Some Other exception");
      }
    try {
        System.out.println("Out of try-catch block...");
    }
   catch(      java.lang.Exception e
                           ){
         e.printStackTrace();
      }
    }

   anException/* a comment */.printStackTrace(); // another comment

   anException /* a comment */
   // another comment

   .printStackTrace();

   }
