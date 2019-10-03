package Especialista;

import javax.ejb.*;

@Remote
// se dice que utilizara conexión remota.
//interface de el ejb

public interface Concurrencia {
  public long Proceso1(long tipo);//declaración de proceso1
  public String Proceso2(long tipo);//declaración de proceso2
}
