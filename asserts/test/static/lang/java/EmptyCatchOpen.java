import java.util;
// This should not be detected
// import java.util.Random;
// import java.lang.Math;
import java.lang.Math.random;

class GenericExceptionsClose{
   public static void main(String args[]){
     try{
         int a[]=new int[7];
         Random $random_gen = new Random();

         a[0] = /* a comment*/
                  // more comments
                  random();
         a[1] = $random_gen /*comment*/
                        .
                        // other comment
                     nextInt(10);
         a[2] = util // comment
                     .Random(); /* util.Random() */
         a[4]=30/0;

         System.out.println("First print statement in try block");
     }
     catch(ArithmeticException e){
        System.out.println("Warning: ArithmeticException");
     }
     catch(ArrayIndexOutOfBoundsException e){
        // Oneline comment
     }
     catch(Exception e){
        /*
        Multiline comment
        Test
        */

        // more comments and an empty line

     } catch          (
        Exception
        e
        )
        {
         // a really weird empty catch
     }
     catch(ArithmeticException e){
        System.out.println("Warning: ArithmeticException");
     }
/*
     try {
           System.out.println("Out of try-catch block...");
  catch(Exception e){
        System.out.println("Warning: Some Other exception");
     }
*/
  }
}
