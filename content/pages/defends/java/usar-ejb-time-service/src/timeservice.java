package fsg;

import java.util.logging.Logger;
import javax.annotation.PostConstruct;
import javax.annotation.Resource;
import javax.ejb.Startup;
import javax.ejb.Timeout;
import javax.ejb.Timer;
import javax.ejb.Singleton;

@Singleton

@Startup

public class TimeService {
  static Logger log = Logger.getLogger("");

  @Resource
  javax.ejb.TimerService timerService;
  public void startTimer(){
    timerService.createTimer(20000, "FLUID Timer");
    log.info("FLUID Timer created at: " + new java.util.Date());
  }

  @Timeout
  public void delayedAction(Timer timer) {
    try {
      log.info("Executing timer: " + timer.getInfo());
      log.info("FLUID Timer action executed at: " + new java.util.Date());
    }
    catch (Exception e) {
      log.warning("Exception while getting timer information");
    }
  }
}
