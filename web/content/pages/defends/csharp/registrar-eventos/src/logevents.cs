using System;
using System.IO;

class Program {
  static void Main(string[] args) {
    writeLog("access.log", "Dangerous behavior");
  }
  private static void writeLog(String file, String message) {
    StreamWriter logFile;
    String logDate = TimeZoneInfo.ConvertTimeToUtc(DateTime.Now)
                     .ToString("ddd, dd MMM yyyy HH':'mm':'ss.fff 'GMT'");
    String log = string.Format("[{0}]: {1}", logDate, message);
    if (!File.Exists(file)) {
      logFile = new StreamWriter(file);
    }

    else {
      logFile = File.AppendText(file);
    }
    logFile.WriteLine(log);
    logFile.Close();
  }
}
