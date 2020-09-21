import java.util.Properties;
import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.rmi.PortableRemoteObject;
import Especialista.Concurrencia;

public class Cliente {
  //Se hace el llamado al metodo Carga que es el que inicia el ejb.
  public void Inicio() {
    long milis=System.currentTimeMillis()+10000;
    System.out.println("inicia Proceso solucion 1");
    carga(milis);
  }

  public static void carga(long i){
     //se hace la conexión al weblogic donde se encuentra el ejb
     Properties prop = new Properties();
     prop.put(Context.INITIAL_CONTEXT_FACTORY,"weblogic.jndi.WLInitialContextFactory");
     //cambiar por la configuracion del servidor de aplicaciones
     prop.put(Context.PROVIDER_URL, "t3://localhost:7001/");
     try {
       //objeto con la información de conexión
       InitialContext contexto = new InitialContext(prop);
       // se le especifica el EJB a ejecutar
       Object obj =
       contexto.lookup("Especialista.Concurrencia#Especialista.Concurrencia");
       Concurrencia Conc = (Concurrencia) PortableRemoteObject.narrow(obj, Concurrencia.class);
       //se utilizan 2 procesos de el ejb como prueba
       long tipo =i;
       long res =Conc.Proceso1(tipo);
       System.out.println("Pasa a proceso 2");
       String res2 =Conc.Proceso2(res+10000);
       System.out.println(res2);
     }
   catch (NamingException e) {
       // evento excepcional a tratar cuando entre a producción.
     }
   }
}
