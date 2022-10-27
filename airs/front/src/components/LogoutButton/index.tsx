/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useAuth0 } from "@auth0/auth0-react";
import React from "react";

const LogoutButton: React.FC = (): JSX.Element => {
  const { isAuthenticated, logout } = useAuth0();

  return isAuthenticated ? (
    <button
      // eslint-disable-next-line react/jsx-no-bind
      onClick={(): void => {
        logout({ returnTo: window.location.origin });
      }}
    >
      {"Log Out"}
    </button>
  ) : (
    <div />
  );
};

export { LogoutButton };
