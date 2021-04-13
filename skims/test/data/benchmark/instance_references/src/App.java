import javax.servlet.http.HttpServletRequest;

public class App {
    public static void main(String[] args) throws Exception {
        float rand = new java.util.Random().nextFloat();

        String cookieName = "testInstanceReference";
        HttpServletRequest request = new HttpServletRequest();

        // this should initialize a new instance to be used in subsequent statements
        User currentUser = new User("Jane Doe");

        currentUser.setUserId(Float.toString(rand));

        String cookieKey = currentUser.getUserId();
        request.getSession().setAttribute(cookieName, cookieKey);
    }

    public void test_01(){
        int rand = new java.util.Random().nextFloat();

        String cookieName = "testInstanceReference";
        HttpServletRequest request = new HttpServletRequest();

        User currentUser = new User("Jane", Float.toString(rand));
        String cookieKey = currentUser.lastName;

        request.getSession().setAttribute(cookieName, cookieKey);
    }

    public void test_02(){
        int rand = new java.util.Random().nextInt();

        HttpServletRequest request = new HttpServletRequest();

        User currentUser = new User("Jane", "Doe", Integer.toString(rand));

        request.getSession().setAttribute("testInstanceReference", currentUser.lastName);
    }

    public void test_03(){
        int rand = new java.util.Random().nextFloat();

        HttpServletRequest request = new HttpServletRequest();

        User currentUser = new User("Jane", "Doe", "xxxxxxxxxx");
        currentUser.userId = Float.toString(rand);

        request.getSession().setAttribute("testInstanceReference", currentUser.getUserId());
    }

}
