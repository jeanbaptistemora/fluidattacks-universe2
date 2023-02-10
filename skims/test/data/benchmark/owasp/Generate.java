public class Generate {
    public static String createRandom() {
        float rand = new java.util.Random().nextFloat();
        return Float.toString(rand).substring(2);
    }

    public static String createSecureRandom() {
        int randNumber = java.security.SecureRandom.getInstance("SHA1PRNG").nextInt(99);
        return Integer.toString(randNumber);
    }

    public static Boolean readFile(String param) {
        String fileName = org.owasp.benchmark.helpers.Utils.TESTFILES_DIR + param;
        java.io.FileInputStream fis = new java.io.FileInputStream(new java.io.File(fileName));
        return true;
    }
}
