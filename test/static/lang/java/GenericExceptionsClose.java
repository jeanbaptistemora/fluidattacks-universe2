import java.security.SecureRandom;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

class GenericExceptionsClose{
   public static void main(String args[]){
     try{
         int a[]=new int[7];
         SecureRandom random = new SecureRandom();
         byte bytes[] = new byte[20];
         a[0]=random.nextBytes(bytes);
         a[4]=30/0;
         System.out.println("First print statement in try block");

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
     }
     catch(ArrayIndexOutOfBoundsException e){
        System.out.println("Warning: ArrayIndexOutOfBoundsException");
     }
     catch (NoSuchAlgorithmException exception) {
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
