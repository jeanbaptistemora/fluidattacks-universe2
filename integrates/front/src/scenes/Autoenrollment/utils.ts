/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Logger } from "utils/logger";

const isPersonalEmail = async (userEmail: string): Promise<boolean> => {
  const url =
    "https://gist.githubusercontent.com/tbrianjones/5992856/raw/93213efb652749e226e69884d6c048e595c1280a/free_email_provider_domains.txt";
  const [, emailDomain] = userEmail.split("@");
  const errorMsg = "Couldn't fetch free email provider domains";

  try {
    const response = await fetch(url);

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

export { isPersonalEmail };
