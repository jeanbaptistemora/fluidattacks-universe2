//normal comment
// int CTE = 3;
/*
   This comment should
   not be detected.
*/

public class Test{
    public int special_add(int a, int b){
        /*
        if(a < 4){
            return 0;
        }
        */
        return a + b;
    }
}
