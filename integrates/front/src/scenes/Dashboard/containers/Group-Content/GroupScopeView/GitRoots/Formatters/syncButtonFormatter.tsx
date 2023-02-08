import { faSyncAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback } from "react";

import { Button } from "components/Button";
import type { IGitRootData } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/types";

interface ISyncButtonFormatterProps {
  row: IGitRootData;
  changeFunction: (arg: IGitRootData) => void;
}

const SyncButtonFormatter: React.FC<ISyncButtonFormatterProps> = ({
  row,
  changeFunction,
}: ISyncButtonFormatterProps): JSX.Element => {
  const handleOnChange = useCallback(
    (ev: React.SyntheticEvent): void => {
      ev.stopPropagation();
      changeFunction(row);
    },
    [changeFunction, row]
  );

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

export const syncButtonFormatter = (
  row: IGitRootData,
  changeFunction: (arg: IGitRootData) => void
): JSX.Element => {
  return <SyncButtonFormatter changeFunction={changeFunction} row={row} />;
};
