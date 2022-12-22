import javax.servlet.http.HttpServletRequest;

public class App {
    private String createRandom() {
        float rand = new java.util.Random().nextFloat();
        return Float.toString(rand).substring(2);
    }

    public static void main(String[] args) throws Exception {
        HttpServletRequest request = new HttpServletRequest();

        float rand = new java.util.Random().nextFloat();

        String cookieName = "testInstanceReference";

        // this should initialize a new instance to be used in subsequent statements
        User currentUser = new User("Jane Doe");

        currentUser.setUserId(Float.toString(rand));

        String cookieKey = currentUser.getUserId();
        request.getSession().setAttribute(cookieName, cookieKey);
    }

    public void test_01() {
        HttpServletRequest request = new HttpServletRequest();

        int rand = new java.util.Random().nextFloat();
        String cookieName = "testInstanceReference";

        User currentUser = new User("Jane", Float.toString(rand));
        String cookieKey = currentUser[lastName];

        request.getSession().setAttribute(cookieName, cookieKey);
    }

    public void test_02() {
        HttpServletRequest request = new HttpServletRequest();

        int rand = new java.util.Random().nextInt();

        User currentUser = new User("Jane", "Doe", Integer.toString(rand));

        request.getSession().setAttribute(cookieName, currentUser[lastName]);
    }

    public void test_03() {
        HttpServletRequest request = new HttpServletRequest();

        int rand = new java.util.Random().nextFloat();

        User currentUser = new User("Jane", "Doe", "xxxxxxxxxx");
        currentUser.userId = Float.toString(rand);

        request.getSession().setAttribute("testInstanceReference", currentUser.getUserId());
    }

    public void test_04() {
        HttpServletRequest request = new HttpServletRequest();

        User currentUser = new User("Jane", "Doe", Generate.createSecureRandom());

        request.getSession().setAttribute("testInstanceReference", currentUser.lastName);
    }

    public void test_05() {
        HttpServletRequest request = new HttpServletRequest();
        String cookieName = "testInstanceReference";

        // this should initialize a new instance to be used in subsequent statements
        User currentUser = new User("Jane Doe");

        currentUser.setUserId(Generate.createRandom());

        String cookieKey = currentUser.getUserId();
        request.getSession().setAttribute(cookieName, cookieKey);
    }

    public void test_06() {
        HttpServletRequest request = new HttpServletRequest();

        String cookieName = "testInstanceReference";
        int rand = new java.util.Random().nextFloat();

        User currentUser = new User("Jane", Float.toString(rand));
        String cookieKey = currentUser[lastName];

        request.getSession().setAttribute(cookieName, cookieKey);
    }

    public void test_07() {
        HttpServletRequest request = new HttpServletRequest();

        int rand = new java.util.Random().nextInt();

        User currentUser = new User("Jane", "Doe", Integer.toString(rand));

        request.getSession().setAttribute(cookieName, currentUser);
    }

    public void test_08() {
        HttpServletRequest request = new HttpServletRequest();

        User currentUser = new User("Jane", "Doe", "xxxxxxxxxx");
        currentUser.userId = this.createRandom();

        request.getSession().setAttribute("testInstanceReference", currentUser.getUserId());
    }

    public void test_09() {
        HttpServletRequest request = new HttpServletRequest();

        String file = request.getParamert("xxxxxxxxxx");
        Generate.readFile(file);
        User currentUser = new User("Jane", "Doe", "xxxxxxxxxxxxx");

        request.getSession().setAttribute("testInstanceReference", currentUser.lastName);
    }

}
