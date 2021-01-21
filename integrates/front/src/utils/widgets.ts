// Third party embeddable scripts not designed for SPAs

export const initializeZendesk: (
  userEmail: string,
  userName: string
) => void = (userEmail, userName): void => {
  const { zE } = window as typeof window & {
    zE: (action: string, event: string, parameters: unknown) => void;
  };
  zE("webWidget", "setLocale", "en-US");
  zE("webWidget", "identify", { email: userEmail, name: userName });
};
