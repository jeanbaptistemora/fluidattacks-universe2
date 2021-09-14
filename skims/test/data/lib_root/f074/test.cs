//normal comment
// int CTE = 3;
/*
   This comment should
   not be detected.
*/
namespace Controllers
{
    public class Calculate
    {
        public static int Sum(int num1, int num2)
        {
            /*
            if(a < 4){
                return 0;
            }
            */
            int total;
            //THis is a sum
            total = num1 + num2;
            return total;
        }
    }
}
