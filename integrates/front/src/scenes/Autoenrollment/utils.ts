import { Buffer } from "buffer";

import _ from "lodash";

import { Logger } from "utils/logger";

const EMAIL_DOMAINS_URL =
  "https://gist.githubusercontent.com/tbrianjones/5992856/raw/93213efb652749e226e69884d6c048e595c1280a/free_email_provider_domains.txt";

const isPersonalEmail = async (userEmail: string): Promise<boolean> => {
  const [, emailDomain] = userEmail.split("@");
  const errorMsg = "Couldn't fetch free email provider domains";

  try {
    const response = await fetch(EMAIL_DOMAINS_URL);

    if (response.status === 200) {
      const text = await response.text();
      const freeEmailDomains = text.split("\n");

      return freeEmailDomains.includes(emailDomain);
    }
    Logger.error(errorMsg, response);

    return true;
  } catch (error) {
    Logger.error(errorMsg, error);

    return true;
  }
};

const getAddGitRootCredentials = (credentials: {
  auth: "TOKEN" | "USER";
  azureOrganization: string | undefined;
  isPat: boolean | undefined;
  key: string;
  name: string;
  password: string;
  token: string;
  type: "" | "HTTPS" | "SSH";
  user: string;
}): Record<string, boolean | string | undefined> | null => {
  if (
    !(
      credentials.key === "" &&
      credentials.user === "" &&
      credentials.password === "" &&
      credentials.token === ""
    )
  ) {
    return {
      azureOrganization:
        _.isUndefined(credentials.azureOrganization) ||
        _.isUndefined(credentials.isPat) ||
        !credentials.isPat
          ? undefined
          : credentials.azureOrganization,
      isPat: _.isUndefined(credentials.isPat) ? false : credentials.isPat,
      key:
        credentials.key === ""
          ? undefined
          : Buffer.from(credentials.key).toString("base64"),
      name: credentials.name,
      password: credentials.password,
      token: credentials.token,
      type: credentials.type,
      user: credentials.user,
    };
  }

  return null;
};

export { EMAIL_DOMAINS_URL, getAddGitRootCredentials, isPersonalEmail };
