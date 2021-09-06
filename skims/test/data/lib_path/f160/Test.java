import java.io.File;

public class Test {
    public static void main(String[] args){
        try {
        System.out.println(File.createTempFile("xxx", null));
        } catch (Exception e) {}
    }
}

/*
 * $ ls -al $(javac Test.java && java Test)
 *
 * -rw-r--r-- 1 kamado kamado 0 Aug 28 14:44 /tmp/xxx948760279845756007.tmp
 *
 */
