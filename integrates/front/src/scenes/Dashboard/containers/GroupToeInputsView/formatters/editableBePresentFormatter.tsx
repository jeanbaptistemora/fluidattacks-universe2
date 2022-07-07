import React from "react";

import type { IToeInputData } from "../types";
import { Switch } from "components/Switch";
import type { IHeaderConfig } from "components/Table/types";
import { translate } from "utils/translations/translate";

const formatBoolean = (value: boolean): string =>
  value
    ? translate.t("group.toe.inputs.yes")
    : translate.t("group.toe.inputs.no");

export const editableBePresentFormatter: (
  canEdit: boolean,
  handleUpdateToeInput: (
    rootId: string,
    component: string,
    entryPoint: string,
    bePresent: boolean
  ) => Promise<void>
) =>
  | ((
      value: boolean,
      row: IToeInputData,
      rowIndex: number,
      key: Readonly<IHeaderConfig>
    ) => JSX.Element | string)
  | undefined = (
  canEdit: boolean,
  handleUpdateAttackedLines: (
    rootId: string,
    component: string,
    entryPoint: string,
    bePresent: boolean
  ) => Promise<void>
):
  | ((
      value: boolean,
      row: IToeInputData,
      rowIndex: number,
      key: Readonly<IHeaderConfig>
    ) => JSX.Element | string)
  | undefined => {
  if (!canEdit) {
    return formatBoolean;
  }

  const formatter: (
    value: boolean,
    row: IToeInputData,
    rowIndex: number,
    key: Readonly<IHeaderConfig>
  ) => JSX.Element = (
    value: boolean,
    row: IToeInputData,
    _rowIndex: number,
    _key: Readonly<IHeaderConfig>
  ): JSX.Element => {
    function handleOnChange(): void {
      void handleUpdateAttackedLines(
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
        onChange={handleOnChange}
      />
    );
  };

  return formatter;
};
