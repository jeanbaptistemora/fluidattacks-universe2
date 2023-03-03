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
@PostMapping("/xmlReader/vuln")
    public String xmlReaderVuln(HttpServletRequest request) {
        try {
            String body = WebUtils.getRequestBody(request);
            logger.info(body);
            // ruleid:owasp.java.xxe.org.xml.sax.XMLReader
            XMLReader xmlReader = XMLReaderFactory.createXMLReader();
            xmlReader.parse(new InputSource(new StringReader(body)));  // parse xml
            return "xmlReader xxe vuln code";
        } catch (Exception e) {
            logger.error(e.toString());
            return EXCEPT;
        }
    }

@PostMapping("/XMLReader/sec")
public String XMLReaderSec(HttpServletRequest request) {
    try {
        String body = WebUtils.getRequestBody(request);
        logger.info(body);
        SAXParserFactory spf = SAXParserFactory.newInstance();
        SAXParser saxParser = spf.newSAXParser();
        XMLReader xmlReader = saxParser.getXMLReader();
        xmlReader.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        xmlReader.setFeature("http://xml.org/sax/features/external-general-entities", false);
        xmlReader.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
        xmlReader.parse(new InputSource(new StringReader(body)));

    } catch (Exception e) {
        logger.error(e.toString());
        return EXCEPT;
    }
    return "XMLReader xxe security code";
}

@RequestMapping(value = "/DocumentBuilder/vuln01", method = RequestMethod.POST)
public String DocumentBuilderVuln01(HttpServletRequest request) {
    try {
        String body = WebUtils.getRequestBody(request);
        logger.info(body);
        // ruleid:owasp.java.xxe.javax.xml.parsers.DocumentBuilderFactory
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        DocumentBuilder db = dbf.newDocumentBuilder();
        StringReader sr = new StringReader(body);
        InputSource is = new InputSource(sr);
        Document document = db.parse(is);  // parse xml

        // 遍历xml节点name和value
        StringBuilder buf = new StringBuilder();
        NodeList rootNodeList = document.getChildNodes();
        for (int i = 0; i < rootNodeList.getLength(); i++) {
            Node rootNode = rootNodeList.item(i);
            NodeList child = rootNode.getChildNodes();
            for (int j = 0; j < child.getLength(); j++) {
                Node node = child.item(j);
                buf.append(String.format("%s: %s\n", node.getNodeName(), node.getTextContent()));
            }
        }
        sr.close();
        return buf.toString();
    } catch (Exception e) {
        logger.error(e.toString());
        return EXCEPT;
    }
}

@RequestMapping(value = "/DocumentBuilder/Sec", method = RequestMethod.POST)
public String DocumentBuilderSec(HttpServletRequest request) {
    try {
        String body = WebUtils.getRequestBody(request);
        logger.info(body);
        // ruleid:owasp.java.xxe.javax.xml.parsers.DocumentBuilderFactory
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
        dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
        DocumentBuilder db = dbf.newDocumentBuilder();
        StringReader sr = new StringReader(body);
        InputSource is = new InputSource(sr);
        db.parse(is);  // parse xml
        sr.close();
    } catch (Exception e) {
        logger.error(e.toString());
        return EXCEPT;
    }
    return "DocumentBuilder xxe security code";
}

}
