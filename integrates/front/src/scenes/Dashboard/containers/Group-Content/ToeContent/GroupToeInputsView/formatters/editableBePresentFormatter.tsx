import React from "react";

import type { IToeInputData } from "../types";
import { Switch } from "components/Switch";
import { translate } from "utils/translations/translate";

function formatBoolean(value: boolean): string {
  return value
    ? translate.t("group.toe.inputs.yes")
    : translate.t("group.toe.inputs.no");
}

export const editableBePresentFormatter = (
  row: IToeInputData,
  canEdit: boolean,
  handleUpdateToeInput: (
    rootId: string,
    component: string,
    entryPoint: string,
    bePresent: boolean
  ) => Promise<void>
): JSX.Element | string => {
  const value: boolean = row.bePresent;

  if (!canEdit) {
    return formatBoolean(value);
  }

  function handleOnChange(): void {
    void handleUpdateToeInput(
      row.rootId,
      row.component,
      row.entryPoint,
      !row.bePresent
    );
  }

  return (
    <Switch
      checked={value}
      label={{
        off: translate.t("group.toe.inputs.no"),
        on: translate.t("group.toe.inputs.yes"),
      }}
      name={"bePresentSwitch"}
      // eslint-disable-next-line
      onChange={handleOnChange} // NOSONAR
    />
  );
};
