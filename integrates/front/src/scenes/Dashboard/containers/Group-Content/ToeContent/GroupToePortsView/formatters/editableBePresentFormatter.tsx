import React from "react";

import type { IToePortData } from "../types";
import { Switch } from "components/Switch";
import { translate } from "utils/translations/translate";

function formatBoolean(value: boolean): string {
  return value
    ? translate.t("group.toe.ports.yes")
    : translate.t("group.toe.ports.no");
}

export const editableBePresentFormatter = (
  row: IToePortData,
  canEdit: boolean,
  handleUpdateToePort: (
    rootId: string,
    address: string,
    port: number,
    bePresent: boolean
  ) => Promise<void>
): JSX.Element | string => {
  const value: boolean = row.bePresent;

  if (!canEdit) {
    return formatBoolean(value);
  }

  function handleOnChange(): void {
    void handleUpdateToePort(row.rootId, row.address, row.port, !row.bePresent);
  }

  return (
    <Switch
      checked={value}
      label={{
        off: translate.t("group.toe.ports.no"),
        on: translate.t("group.toe.ports.yes"),
      }}
      name={"bePresentSwitch"}
      onChange={handleOnChange}
    />
  );
};
