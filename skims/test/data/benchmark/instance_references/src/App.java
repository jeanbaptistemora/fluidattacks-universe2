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
}
