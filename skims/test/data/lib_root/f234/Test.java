public class Test{
    public static void main(String[] args){
        try {
            throw new IOException();
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }
}
