// Third party embeddable scripts not designed for SPAs

const initializeDelighted: (userEmail: string, userName: string) => void = (
  userEmail,
  userName
): void => {
  const { delighted } = window as typeof window & {
    delighted: {
      survey: (options: Record<string, unknown>) => void;
    };
  };
  if (!userEmail.endsWith("@fluidattacks.com")) {
    delighted.survey({
      email: userEmail,
      initialDelay: 45,
      name: userName,
      recurringPeriod: 2592000,
    });
  }
};

const initializeZendesk: (userEmail: string, userName: string) => void = (
  userEmail,
  userName
): void => {
  const { zE } = window as typeof window & {
    zE: (action: string, event: string, parameters: unknown) => void;
  };
  zE("webWidget", "setLocale", "en-US");
  zE("webWidget", "identify", { email: userEmail, name: userName });
};

export { initializeDelighted, initializeZendesk };
