import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.parsers.SAXParser;


public class XXE {

  private static Logger logger = LoggerFactory.getLogger(XXE.class);
  private static String EXCEPT = "xxe except";


@RequestMapping(value = "/SAXParser/vuln", method = RequestMethod.POST)
public String SAXParserVuln(HttpServletRequest request) {
    try {
        String body = WebUtils.getRequestBody(request);
        logger.info(body);
        // ruleid:owasp.java.xxe.javax.xml.parsers.SAXParserFactory
        SAXParserFactory spf = SAXParserFactory.newInstance();
        SAXParser parser = spf.newSAXParser();
        parser.parse(new InputSource(new StringReader(body)), new DefaultHandler());  // parse xml

        return "SAXParser xxe vuln code";
    } catch (Exception e) {
        logger.error(e.toString());
        return EXCEPT;
    }
}



@RequestMapping(value = "/SAXParser/sec", method = RequestMethod.POST)
public String SAXParserSec(HttpServletRequest request) {
    try {
        String body = WebUtils.getRequestBody(request);
        logger.info(body);
        SAXParserFactory spf = SAXParserFactory.newInstance();
        spf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        spf.setFeature("http://xml.org/sax/features/external-general-entities", false);
        spf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
        SAXParser parser = spf.newSAXParser();
        parser.parse(new InputSource(new StringReader(body)), new DefaultHandler());  // parse xml
    } catch (Exception e) {
        logger.error(e.toString());
        return EXCEPT;
    }
    return "SAXParser xxe security code";
}
}
