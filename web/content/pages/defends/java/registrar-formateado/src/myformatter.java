import java.util.logging.Formatter;
import java.util.logging.LogRecord;

public class MyFormatter extends Formatter
{
  public String format(LogRecord record)
  {
    return("MyFormatter: " + record.getLevel().intValue()+ " - " + record.getMessage() + System.getProperty("line.separator"));
  }
}
