import java.io.FileInputStream;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;

public class Test {


    public static void main(String[] args) {
        new Test().readData();
    }
    
    public void readData(){

            int bufferSize = 16 * 1024;
            byte[] zeroes = new byte[bufferSize];
            ByteBuffer buffer = ByteBuffer.allocateDirect(bufferSize);

            try (FileChannel rdr = (new FileInputStream("file")).getChannel()) {

              while (rdr.read(buffer) > 0) {

                // Hacer algo con el búfer

                buffer.clear();
                buffer.put(zeroes); // sobrescribir el búfer con ceros
                buffer.clear();
              }

            } catch (Throwable e) {
              // Manejar el error
            }

    }
        
}