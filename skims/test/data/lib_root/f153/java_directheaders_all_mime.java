public class test112 extends HttpServlet {

  // Line 4 should be marked
  Header myHeader = new Header("Accept", "*/*");

  // Line 6 is safe
  Header myHeaderII = new Header("Accept","text/html");

}
