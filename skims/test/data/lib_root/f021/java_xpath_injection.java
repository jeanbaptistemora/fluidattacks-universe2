import java.io.IOException;
import javax.servlet.http.HttpServletRequest;

public class test21 extends HttpServlet {

  public void runUnsafe(HttpServletRequest request, HttpServletResponse response) throws IOException {

    String param = request.getHeader("someheader");
    javax.xml.parsers.DocumentBuilder builder = builderFactory.newDocumentBuilder();
    org.w3c.dom.Document xmlDocument = builder.parse(file);
    javax.xml.xpath.XPathFactory xpf = javax.xml.xpath.XPathFactory.newInstance();
    javax.xml.xpath.XPath xp = xpf.newXPath();

    String expression = "/Employees/Employee[@emplid='"+param+"']";
    String result = xp.evaluate(expression, xmlDocument);

  }

}
