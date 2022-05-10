import { useMutation, useQuery } from "@apollo/client";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { AUTOENROLL_DEMO, GET_USER_WELCOME } from "./queries";
import type { IAutoenrollDemoResult, IGetUserWelcomeResult } from "./types";

import { Dashboard } from "scenes/Dashboard";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const Welcome: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const [browsingDemo, setBrowsingDemo] = useState(false);

  const { data, loading } = useQuery<IGetUserWelcomeResult>(GET_USER_WELCOME, {
    onError: (error): void => {
      error.graphQLErrors.forEach(({ message }): void => {
        Logger.error("An error occurred loading user welcome", message);
      });
    },
  });

  const [autoenrollDemo] = useMutation<IAutoenrollDemoResult>(AUTOENROLL_DEMO, {
    awaitRefetchQueries: true,
    onCompleted: (result): void => {
      if (result.autoenrollDemo.success) {
        setBrowsingDemo(true);
      }
    },
    onError: (error): void => {
      error.graphQLErrors.forEach(({ message }): void => {
        if (
          message ===
          "Exception - User belongs to existing organizations and cannot enroll to demo"
        ) {
          msgError(t("sidebar.newOrganization.modal.invalidName"));
        } else {
          Logger.error("An error occurred creating new organization", message);
        }
      });
    },
    refetchQueries: [GET_USER_WELCOME],
  });

  const enrollToDemo = useCallback(async (): Promise<void> => {
    await autoenrollDemo();
    localStorage.clear();
    sessionStorage.clear();
  }, [autoenrollDemo]);

  const goToDemo = useCallback((): void => {
    void enrollToDemo();
  }, [enrollToDemo]);

  if (loading) {
    return <div />;
  }

  const organizations = data === undefined ? [] : data.me.organizations;
  const isFirstTimeUser = organizations.length === 0;

  if (isFirstTimeUser && !browsingDemo) {
    goToDemo();

    return <div />;
  }

  return <Dashboard />;
};

export { Welcome };
