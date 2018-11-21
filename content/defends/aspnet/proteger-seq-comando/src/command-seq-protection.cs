using System;
using System.Web;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

class Protecthtmli {

  public static void Main() {
    TextBox TextBox1 = new TextBox();
    TextBox1.ID = "textBox1";
    TextBox1.Text = "No <HTML> injections allowed!";
    Controls.Add(TextBox1);

    Private void Button1_Click(object sender, System.EventArgs e) {
      Label1.Text = Server.HtmlEncode(TextBox1.Text);
      Label2.Text = Server.HtmlEncode(dsCustomers1.Customers[0].CompanyName);
    }
  }

}
