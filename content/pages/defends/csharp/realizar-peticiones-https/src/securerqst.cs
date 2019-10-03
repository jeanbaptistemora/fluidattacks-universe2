using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Security.Cryptography;
using System.Net;

namespace ConsoleApplication1 {
  class Program {
    static void Main(string[] args) {
      string post_data = "foo=bar&baz=oof";
      string uri = "https://www.verisign.com/";
      HttpWebRequest request = (HttpWebRequest)
      WebRequest.Create(uri);
      request.KeepAlive = false;
      request.ProtocolVersion = HttpVersion.Version10;
      request.Method = "POST";
      byte[] postBytes = Encoding.ASCII.GetBytes(post_data);
      request.ContentType = "application/x-www-form-urlencoded";
      request.ContentLength = postBytes.Length;
      Stream requestStream = request.GetRequestStream();
      requestStream.Write(postBytes, 0, postBytes.Length);
      requestStream.Close();
      HttpWebResponse response = (HttpWebResponse)request.GetResponse();
      Console.WriteLine(new StreamReader(response.GetResponseStream()).ReadToEnd());
      Console.WriteLine(response.StatusCode);
      //For custom certificates:
      System.Net.ServicePointManager.CertificatePolicy = new MyPolicy();
    }
  }
}
