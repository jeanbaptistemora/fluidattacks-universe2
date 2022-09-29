/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faSyncAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React from "react";

import { Button } from "components/Button";
import type { IGitRootData } from "scenes/Dashboard/containers/GroupScopeView/types";

export const syncButtonFormatter = (
  row: IGitRootData,
  changeFunction: (arg: IGitRootData) => void
): JSX.Element => {
  function handleOnChange(ev: React.SyntheticEvent): void {
    ev.stopPropagation();
    changeFunction(row);
  }

  return (
    <Button
      disabled={
        row.state !== "ACTIVE" ||
        _.isNull(row.credentials) ||
        (!_.isNull(row.credentials) && row.credentials.name === "")
      }
      id={"gitRootSync"}
      onClick={handleOnChange}
      variant={"secondary"}
    >
      <FontAwesomeIcon icon={faSyncAlt} />
    </Button>
  );
};
