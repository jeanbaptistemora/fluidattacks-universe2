import { faSyncAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React from "react";

import { Button } from "components/Button";
import type { IGitRootData } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/types";

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
      // eslint-disable-next-line
      onClick={handleOnChange} // NOSONAR
      variant={"secondary"}
    >
      <FontAwesomeIcon icon={faSyncAlt} />
    </Button>
  );
};
