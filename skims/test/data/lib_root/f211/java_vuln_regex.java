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
public boolean validate(javax.servlet.http.HttpServletRequest request) {
  String regex = "(A+)+";
  String input = "hello";

  input.matches(regex);  // Safe
}

public boolean validate(javax.servlet.http.HttpServletRequest request) {
  String regex = "[a-zA-Z0-9]+";
  String input = request.getParameter("input");

  input.matches(regex);  // Safe
}

public boolean validate(Object personal_object) {
  String regex = "(A+)+";
  String input = personal_object.getParameter(1);

  input.matches(regex);  // Safe
}

public boolean validate(Object personal_object) {
  String regex = "(A+)+";
  String input = personal_object.getParameter(1);

  input.matches(regex);  // Safe
}

public boolean isValid (String alphanumericField,
  ConstraintValidatorContext cxt) {
  Pattern pattern = Pattern.compile(USERNAME_PATTERN);
  return pattern.matcher(alphanumericField).matches();
}

}
