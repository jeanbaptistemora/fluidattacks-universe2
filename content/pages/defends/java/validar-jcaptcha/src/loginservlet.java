package com.servlet.servletidentifies;

import com.octo.captcha.service.CaptchaServiceException;
import javax.servlet.*;
import javax.servlet.http.*;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.Map;
import javax.imageio.ImageIO;

public class LoginServlet extends HttpServlet
{
  String sImgType = null;
  public void init( ServletConfig servletConfig ) throws ServletException
  {
    super.init( servletConfig );
    sImgType = servletConfig.getInitParameter( "ImageType" );
    sImgType = sImgType==null ? "png" : sImgType.trim().toLowerCase();
    if ( !sImgType.equalsIgnoreCase("png") && !sImgType.equalsIgnoreCase("jpg") &&
       !sImgType.equalsIgnoreCase("jpeg") )
    {
      sImgType = "png";
    }
  }
  protected void doGet( HttpServletRequest request, HttpServletResponse response )
    throws ServletException, IOException
  {
    ByteArrayOutputStream imgOutputStream = new ByteArrayOutputStream();
    byte[] captchaBytes;
    try
    {
      String identificadorCaptcha = request.getSession().getId();
      // Generar la imagen captcha en base al identificador especificado
      BufferedImage challengeImage = ServicioCaptcha.getInstance()
       .getImageChallengeForID(captchaId, request.getLocale() );
      ImageIO.write( challengeImage, sImgType, imgOutputStream );
      captchaBytes = imgOutputStream.toByteArray();
    }
    catch( CaptchaServiceException cse )
    {
      response.sendError( HttpServletResponse.SC_INTERNAL_SERVER_ERROR,
        "Error generando la imagen captcha" );
      return;
    }
    catch( IOException ioe )
    {
       response.sendError( HttpServletResponse.SC_INTERNAL_SERVER_ERROR,
          "Error generando la imagen captcha" );
       return;
    }
    response.setHeader( "Cache-Control", "no-store" );
    response.setHeader( "Pragma", "no-cache" );
    response.setDateHeader( "Expires", 0 );
    response.setContentType( "image/" + (sImgType.equalsIgnoreCase("png") ? "png" : "jpeg"));
    // Se despliega la imagen al usuario.
    ServletOutputStream outStream = response.getOutputStream();
    outStream.write( captchaBytes );
    outStream.flush();
    outStream.close();
  }

  protected void doPost( HttpServletRequest request, HttpServletResponse response )
    throws ServletException, IOException
    {
      // Se obtienen los parámetros involucrados en la solicitud
      Map paramMap = request.getParameterMap();
      String[] valorCaptcha = (String[])paramMap.get( "valorCaptcha" );
      String sessId = request.getSession().getId();
      String textoCaptcha = valorCaptcha.length>0 ? valorCaptcha[0] : "";
      // Se verifica si el texto ingresado por el usuario corresponde con el
      // contenido mostrado en la imagen
      boolean estadoCaptcha =ServicioCaptcha.getInstance().validateResponseForID(
      sessId, textoCaptcha );
      if (estadoCaptcha)
      {
        // Captcha verificado correctamente
      }
      else
      {
        // Captcha invalido
      }
   }
}
