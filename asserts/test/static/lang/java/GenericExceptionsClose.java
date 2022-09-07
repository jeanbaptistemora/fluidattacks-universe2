// SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
//
// SPDX-License-Identifier: MPL-2.0

import java.security.SecureRandom;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

class GenericExceptionsClose{
   public static void main(String args[]) throws IOExceptions, SQLException{
     try{
         int a[]=new int[1024];
         SecureRandom random = new SecureRandom();
         byte bytes[] = new byte[20];
         android.permission.BLUETOOTH
         a[0]=random.nextBytes(bytes);
         a[4]=30/0;
         System.out.println("First print statement in try block");
         String api = "https://fluidattacks.com"
         MessageDigest messageDigest, messageDigest2;
         messageDigest = MessageDigest.getInstance("SHA-256");
         messageDigest.update(data.getBytes());
         byte[] messageDigestSHA256 = messageDigest.digest();

         Cipher aes = Cipher.getInstance("AES/GCM/PKCS5Padding");

         Cipher aes = Cipher // a comment
                     /*another comment*/          .getInstance(
                  "AES/CBC/NoPadding" // a comment
                  /* A comment */
                  TheProviderAsAVar /* A comment */
                  );         aes.init(Cipher.ENCRYPT_MODE, secretKeySpec);

         Cipher rsa = Cipher // a comment
                  /*another comment*/          .getInstance(
               "RSA/CBC/OAEPWITHSHA-256ANDMGF1PADDING" // a comment
               /* A comment */
               TheProviderAsAVar /* A comment */
               );

         Cipher rsa = Cipher // a comment
                  /*another comment*/          .getInstance(
               "RSA/CBC/OAEPpadding" // a comment
               /* A comment */
               TheProviderAsAVar /* A comment */
               );

         Cipher rsa = Cipher // a comment
                  /*another comment*/          .getInstance(
               "RSa/CbC/OAEPPadding" // a comment
               /* A comment */
               TheProviderAsAVar /* A comment */
               );

         SSLContext.getInstance("tlsv1.2");


         KeyPairGenerator key2 = KeyPairGenerator.getInstance("DSA");

         var instance = SSLContext.getInstance(  // a comment
               "DTLSv1.3" /* A comment */
               // a comment
               );
         key2.initialize(
            3125 /* A comment */
            );

         @RequestMapping(value = "*", // a comment
         method = {
             GET})

         @RequestMapping(value = "*",
          method = GET /* A comment */
          )
         byte[] encrypted = aes.doFinal(input.getBytes("UTF-8"));

         if (a[0] > 200) {
            System.out.println("Big num");
         } else  if (a[0] < 100){
            System.out.println("Small num");
            // This comment should not comment the else clause
         } else {
            System.out.println("Average num");
         }
     }
     catch(ArithmeticException e){
        System.out.println("Warning: ArithmeticException");
        throw SQLException(
           "invalid credentials"
           )
     }
     catch(ArrayIndexOutOfBoundsException e){
        System.out.println("Warning: ArrayIndexOutOfBoundsException");
     }
     catch (NoSuchAlgorithmException exception) {
        throw InvocationTargetException("Invalid Object")
        System.out.println("Warning: NoSuchAlgorithmException");
     }
/*
     try {
           System.out.println("Out of try-catch block...");
           int a = Math.random();
           if (a[0] > 200) {
              System.out.println("Big num");
           }
  catch(Exception e){
        System.out.println("Warning: Some Other exception");
     }
*/
  }
}
