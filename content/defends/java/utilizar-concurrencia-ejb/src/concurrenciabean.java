package Especialista;

import javax.ejb.*;

@Remote(Concurrencia.class)

@Stateless (mappedName="Especialista/Concurrencia" )

public class ConcurrenciaBean {

 //proceso de prueba numero 1, hace un retardo en tiempo para simular una transacción
  public long Proceso1(long tipo){
    boolean evento = false;
    while(evento==false)
    {
      if (System.currentTimeMillis() >= tipo)
      {
        evento=true;
      }
    else{
        System.out.println("Procesando......");
      }
    }
    long milis =System.currentTimeMillis();
    return milis;
  }

   //proceso de prueba numero 2, hace un retardo en tiempo para simular una transacción
   public String Proceso2(long tipo){
     boolean evento = false;
     while(evento==false)
     {
       if (System.currentTimeMillis() >= tipo)
       {
         evento=true;
       }
     else {
         System.out.println("Procesando222222......");
       }
     }
     return "Fin Proceso";
   }
}
