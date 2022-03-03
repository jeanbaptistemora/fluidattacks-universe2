import { faSyncAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { Button } from "components/Button";
import type { IHeaderConfig } from "components/DataTableNext/types";
import type { IGitRootAttr } from "scenes/Dashboard/containers/GroupScopeView/types";

export const syncButtonFormatter: (
  value: string,
  row: Readonly<IGitRootAttr>,
  rowIndex: number,
  key: Readonly<IHeaderConfig>
) => JSX.Element = (
  _value: string,
  row: Readonly<IGitRootAttr>,
  _rowIndex: number,
  key: Readonly<IHeaderConfig>
): JSX.Element => {
  function handleOnChange(ev: React.SyntheticEvent): void {
    ev.stopPropagation();
    if (key.changeFunction !== undefined) {
      key.changeFunction(row as unknown as Record<string, string>);
    }
  }

  return (
    <Button
      disabled={row.state !== "ACTIVE" || row.credentials.name === ""}
      id={"gitRootSync"}
      onClick={handleOnChange}
      variant={"secondary"}
    >
      <FontAwesomeIcon icon={faSyncAlt} />
    </Button>
  );
};
