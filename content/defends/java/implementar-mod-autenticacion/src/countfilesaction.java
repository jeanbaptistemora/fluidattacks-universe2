import java.io.*;
import java.security.*;

public class CountFilesAction implements PrivilegedAction {
  private String directory;
  public CountFilesAction(String d) {
    directory = d;
  }
  public Object run() {
    File f = new File(directory);
    File fArray[] = f.listFiles();
    return new Integer(fArray.length);
  }
}
