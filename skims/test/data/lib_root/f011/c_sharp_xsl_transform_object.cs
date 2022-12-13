using System;
using System.Xml;
using System.Xml.XPath;
using System.Xml.Xsl;

namespace TestForXslTransform
{
    class Program
    {
        static void Main(string[] args)
        {
            XslTransform xslt = new XslTransform();
            xslt.Load("https://server/favorite.xsl");
            XPathDocument mydata = new XPathDocument("inputdata.xml");
            XmlWriter writer = new XmlTextWriter(Console.Out);
            xslt.Transform(mydata, null, writer, null);
        }
    }
}
