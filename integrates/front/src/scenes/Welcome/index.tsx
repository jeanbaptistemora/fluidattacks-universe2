import { useQuery } from "@apollo/client";
import Bugsnag from "@bugsnag/js";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { GET_USER_WELCOME } from "./queries";
import type { IGetUserWelcomeResult } from "./types";
import { isPersonalEmail } from "./utils";

import { Announce } from "components/Announce";
import { Autoenrollment } from "scenes/Autoenrollment";
import { Dashboard } from "scenes/Dashboard";
import { Logger } from "utils/logger";
import { initializeZendesk } from "utils/widgets";

const Welcome: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const [hasPersonalEmail, setHasPersonalEmail] = useState<boolean | undefined>(
    undefined
  );

  const { data, loading } = useQuery<IGetUserWelcomeResult>(GET_USER_WELCOME, {
    onCompleted: async ({ me }): Promise<void> => {
      Bugsnag.setUser(me.userEmail, me.userEmail, me.userName);
      mixpanel.identify(me.userEmail);
      mixpanel.register({
        User: me.userName,
        // Intentional snake case
        // eslint-disable-next-line camelcase
        integrates_user_email: me.userEmail,
      });
      mixpanel.people.set({ $email: me.userEmail, $name: me.userName });
      initializeZendesk(me.userEmail, me.userName);
      setHasPersonalEmail(await isPersonalEmail(me.userEmail));
    },
    onError: (error): void => {
      error.graphQLErrors.forEach(({ message }): void => {
        Logger.error("An error occurred loading user welcome", message);
      });
    },
  });

  if (loading) {
    return <div />;
  }

  const organizations = data === undefined ? [] : data.me.organizations;
  const isFirstTimeUser = organizations.length === 0;

  if (isFirstTimeUser) {
    if (hasPersonalEmail === undefined) {
      return <div />;
    }

    if (hasPersonalEmail) {
      return <Announce message={t("autoenrollment.corporateOnly")} />;
    }

    return <Autoenrollment />;
  }

  return <Dashboard />;
};

export { Welcome };
