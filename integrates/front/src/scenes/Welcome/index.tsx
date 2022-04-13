import { useQuery } from "@apollo/client";
import React, { useCallback, useState } from "react";
import { useHistory } from "react-router-dom";

import { Onboarding } from "./Onboarding";
import { GET_USER_WELCOME } from "./queries";
import type { IGetUserWelcomeResult } from "./types";

import { Dashboard } from "scenes/Dashboard";

const Welcome: React.FC = (): JSX.Element => {
  const [browsingDemo, setBrowsingDemo] = useState(false);
  const goToDemo = useCallback((): void => {
    setBrowsingDemo(true);
  }, []);

  const { push } = useHistory();
  const goToTour = useCallback((): void => {
    push("/welcome/tour");
  }, [push]);

  const { data, loading } = useQuery<IGetUserWelcomeResult>(GET_USER_WELCOME);

  if (loading) {
    return <div />;
  }

  const organizations = data === undefined ? [] : [{ name: "imamura" }];
  const isFirstTimeUser =
    organizations.length === 1 &&
    organizations[0].name.toLowerCase() === "imamura";

  if (isFirstTimeUser && !browsingDemo) {
    return <Onboarding goToDemo={goToDemo} goToTour={goToTour} />;
  }

  return <Dashboard />;
};

export { Welcome };
