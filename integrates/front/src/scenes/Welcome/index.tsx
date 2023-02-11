import { useQuery } from "@apollo/client";
import Bugsnag from "@bugsnag/js";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React from "react";

import { GET_STAKEHOLDER_ENROLLMENT } from "./queries";
import type { IGetStakeholderEnrollmentResult } from "./types";

import { Autoenrollment } from "scenes/Autoenrollment";
import { Dashboard } from "scenes/Dashboard";
import { NoEnrolledUser } from "scenes/Login/NoEnrolledUser";
import { EnrolledUser } from "scenes/SignUp/Components/EnrolledUser";
import { Logger } from "utils/logger";
import { initializeZendesk } from "utils/widgets";

const Welcome: React.FC = (): JSX.Element => {
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

  const isEnrolled: boolean = data.me.enrolled;
  const validManaged = ["NOT_MANAGED", "MANAGED", "TRIAL"];
  const subscribedOrgs = data.me.organizations.filter(
    (org): boolean =>
      org.groups.filter((group): boolean =>
        validManaged.includes(group.managed)
      ).length > 0
  );

  if (isEnrolled) {
    if (sessionStorage.getItem("trial") === "true") {
      return <EnrolledUser />;
    }
    if (
      data.me.trial === null ||
      !(data.me.trial.completed && subscribedOrgs.length === 0)
    ) {
      return <Dashboard />;
    }
  }

  if (sessionStorage.getItem("trial") === "true") {
    return <Autoenrollment />;
  }

  return <NoEnrolledUser />;
};

export { Welcome };
