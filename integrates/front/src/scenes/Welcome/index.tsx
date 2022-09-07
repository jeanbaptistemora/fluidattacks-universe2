/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useLazyQuery, useQuery } from "@apollo/client";
import Bugsnag from "@bugsnag/js";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { GET_STAKEHOLDER_ENROLLMENT, GET_STAKEHOLDER_WELCOME } from "./queries";
import type {
  IGetStakeholderEnrollmentResult,
  IGetStakeholderWelcomeResult,
} from "./types";
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
  const [isEnrolled, setIsEnrolled] = useState<boolean | undefined>(undefined);

  const [getStakeholderWelcome, { data: welcomeData }] =
    useLazyQuery<IGetStakeholderWelcomeResult>(GET_STAKEHOLDER_WELCOME, {
      onCompleted: async ({ me }): Promise<void> => {
        setHasPersonalEmail(await isPersonalEmail(me.userEmail));
      },
      onError: (error): void => {
        error.graphQLErrors.forEach(({ message }): void => {
          Logger.error(
            "An error occurred loading stakeholder welcome",
            message
          );
        });
      },
    });
  const { data: enrollmentData } = useQuery<IGetStakeholderEnrollmentResult>(
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

        if (me.enrollment.enrolled) {
          setIsEnrolled(true);
        } else {
          getStakeholderWelcome();
        }
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

  if (_.isUndefined(enrollmentData)) {
    return <div />;
  }

  if (!_.isUndefined(isEnrolled) && isEnrolled) {
    return <Dashboard />;
  }

  if (_.isUndefined(welcomeData)) {
    return <div />;
  }

  if (
    welcomeData.me.organizations.length > 0 &&
    welcomeData.me.organizations[0].groups.length > 0
  ) {
    return (
      <Autoenrollment
        group={welcomeData.me.organizations[0].groups[0].name}
        organization={welcomeData.me.organizations[0].name}
      />
    );
  }

  if (welcomeData.me.organizations.length > 0) {
    return (
      <Autoenrollment organization={welcomeData.me.organizations[0].name} />
    );
  }

  if (_.isUndefined(hasPersonalEmail)) {
    return <div />;
  }

  if (hasPersonalEmail) {
    return <Announce message={t("autoenrollment.corporateOnly")} />;
  }

  return <Autoenrollment />;
};

export { Welcome };
