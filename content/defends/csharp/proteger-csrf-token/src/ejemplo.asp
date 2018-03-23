<%@ Page Language="C#" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<script runat="server">
  protected void Page_Load(object sender, EventArgs e) {
    //Se verifica que sea la primer vez que se carga el sitio
    if (!Page.IsPostBack) {
      //Se crea el token
      string CSRF_Token = System.Guid.NewGuid().ToString();

      //Se utiliza como identificador del Token dentro de la sesión, el nombre de la página en la que se encuentra  actualmente
      string page_name = System.IO.Path.GetFileName(HttpContext.Current.Request.Url.AbsolutePath);
      string page_token = page_name + "_ID";

      //Se guarda el Token generado en la sesión, con el identificador que se generó anteriormente para su futura busqueda
      HttpContext.Current.Session[page_token] = CSRF_Token;

      //Se asigna el Token al valor del campo oculto del formulario, que para efectos prácticos se le ha dado el nombre de Token
      Token.Value = CSRF_Token;
    }
  }

  public void submit(object sender, EventArgs e) {
    //Se verifica que el valor del Token almacenado en sesión, sea igual al valor del campo oculto en el formulario
    string Page_Token = System.IO.Path.GetFileName(HttpContext.Current.Request.Url.AbsolutePath) + "_ID";

    if (Token.Value.ToString() != HttpContext.Current.Session[Page_Token].ToString()) {
      //De no ser los mismos, se cierra limpia y cierra la sesión, y se redirige hacia otro sitio web
      HttpContext.Current.Session.Abandon();
      HttpContext.Current.Session.Clear();
      Response.Redirect("...");
    } else {
      //De ser iguales los valores, se sigue con la ejecución de las instrucciones posteriores al envío de la información
    }
  }
</script>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head id="Head1" runat="server">
      <title>Calendar Example</title>
  </head>
  <body>
    <form id="form1" runat="server">
      <asp:HiddenField ID="Token" runat="server" />
      <asp:Button ID="btn" Text="Submit" runat="server" OnClick="submit" />
    </form>
  </body>
</html>
