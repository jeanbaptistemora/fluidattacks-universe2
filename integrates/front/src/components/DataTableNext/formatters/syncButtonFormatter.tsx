import { faSyncAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { Button } from "components/Button";
import type { IHeaderConfig } from "components/DataTableNext/types";

export const syncButtonFormatter: (
  value: string,
  row: Readonly<Record<string, string>>,
  rowIndex: number,
  key: Readonly<IHeaderConfig>
) => JSX.Element = (
  _value: string,
  row: Readonly<Record<string, string>>,
  _rowIndex: number,
  key: Readonly<IHeaderConfig>
): JSX.Element => {
  function handleOnChange(ev: React.SyntheticEvent): void {
    ev.stopPropagation();
    if (key.changeFunction !== undefined) {
      key.changeFunction(row);
    }
  }

  return (
    <Button
      disabled={row.state !== "ACTIVE"}
      id={"gitRootSync"}
      onClick={handleOnChange}
    >
      <FontAwesomeIcon icon={faSyncAlt} />
    </Button>
  );
};
