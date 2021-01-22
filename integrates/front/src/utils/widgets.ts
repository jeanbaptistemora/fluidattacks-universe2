// Third party embeddable scripts not designed for SPAs

import { Logger } from "./logger";

const initializeDelighted: (userEmail: string, userName: string) => void = (
  userEmail,
  userName
): void => {
  const { delighted } = window as typeof window & {
    delighted?: {
      survey: (options: Record<string, unknown>) => void;
    };
  };

  if (delighted) {
    if (!userEmail.endsWith("@fluidattacks.com")) {
      delighted.survey({
        email: userEmail,
        initialDelay: 45,
        name: userName,
        recurringPeriod: 2592000,
      });
    }
  } else {
    Logger.warning("Couldn't initialize delighted");
  }
};

const initializeZendesk: (userEmail: string, userName: string) => void = (
  userEmail,
  userName
): void => {
  const { zE } = window as typeof window & {
    zE?: (action: string, event: string, parameters: unknown) => void;
  };

  if (zE) {
    zE("webWidget", "setLocale", "en-US");
    zE("webWidget", "identify", { email: userEmail, name: userName });
  } else {
    Logger.warning("Couldn't initialize zendesk");
  }
};

export { initializeDelighted, initializeZendesk };
