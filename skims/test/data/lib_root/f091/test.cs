using System;
using Microsoft.AspNetCore.Mvc;

public class RSPEC5145LogInjectionLog4NetNoncompliantController : Controller
{
    public void LogSomething(HttpRequest id)
    {
        //insecure
        private static readonly log4net.ILog _logger = log4net.LogManager.GetLogger();
        _logger.Info(id);

        //insecure
        var logger = new DBLogger();
        logger.Log(id);

        //insecure
        var log = new FileLogger();
        log.Debug(id);

        //secure
        private static readonly log4net.ILog sec_log = log4net.LogManager.GetLogger();
        id = id.Replace('\n', '_').Replace('\r', '_').Replace('\t', '_');
        sec_log.Info(id);
    }
}
