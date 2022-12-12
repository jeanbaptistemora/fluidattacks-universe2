public class Test{
public boolean validate(javax.servlet.http.HttpServletRequest request) {
  String regex = "(A+)+";
  String input = request.getParameter("input");

  input.matches(regex);  // Not-safe
}

public boolean validate(javax.servlet.http.HttpServletRequest request) {
  String regex = "(A+)+";
  String input = request.getParameter("input");

  input.matches(Pattern.quote(regex));  // Safe

}

public boolean validate(javax.servlet.http.HttpServletRequest request) {
  String regex = Pattern.quote("(A+)+");
  String input = request.getParameter("input");

  input.matches(regex);  // Safe

}

}
