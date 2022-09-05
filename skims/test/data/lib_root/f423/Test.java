public class Test{
    public static void main(String[] args){
        System.exit(0);
        Runtime.getRuntime().exit(0);
        Runtime.getRuntime().halt(0);
        try {
            throw new IOException();
        }
        catch (IOException e) {
            System.exit(0);
        }
    }
    public static void test(String[] args){
        System.exit(0);
        Runtime.getRuntime().exit(0);
        Runtime.getRuntime().halt(0);
    }
}
System.exit(0);
Runtime.getRuntime().exit(0);
Runtime.getRuntime().halt(0);
