/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useQuery } from "@apollo/client";
import Bugsnag from "@bugsnag/js";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React from "react";
import { useTranslation } from "react-i18next";
import { useLocation } from "react-router-dom";

import { GET_STAKEHOLDER_ENROLLMENT } from "./queries";
import type { IGetStakeholderEnrollmentResult } from "./types";

import { Announce } from "components/Announce";
import { Autoenrollment } from "scenes/Autoenrollment";
import { Dashboard } from "scenes/Dashboard";
import { Logger } from "utils/logger";
import { initializeZendesk } from "utils/widgets";

const Welcome: React.FC = (): JSX.Element => {
  const { hash } = useLocation();
  const { t } = useTranslation();

  const { data } = useQuery<IGetStakeholderEnrollmentResult>(
    GET_STAKEHOLDER_ENROLLMENT,
    {
      fetchPolicy: "cache-first",
      onCompleted: ({ me }): void => {
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
      },
      onError: (error): void => {
        error.graphQLErrors.forEach(({ message }): void => {
          Logger.error(
            "An error occurred loading stakeholder enrollment",
            message
          );
        });
      },
    }
  );

  if (data === undefined) {
    return <div />;
  }

  const isEnrolled = data.me.enrollment.enrolled;

  if (isEnrolled) {
    if (hash === "#trial") {
      return <Announce message={t("autoenrollment.notElegible")} />;
    }

    return <Dashboard />;
  }

  return <Autoenrollment />;
};

export { Welcome };
