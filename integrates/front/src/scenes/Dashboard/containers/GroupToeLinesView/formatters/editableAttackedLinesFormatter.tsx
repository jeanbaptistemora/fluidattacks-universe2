/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/no-autofocus */
import _ from "lodash";
import React from "react";

import type { IToeLinesData } from "../types";
import { NumberInput } from "components/NumberInput";
import type { IHeaderConfig } from "components/Table/types";
import { translate } from "utils/translations/translate";

export const editableAttackedLinesFormatter: (
  canEdit: boolean,
  handleUpdateAttackedLines: (
    rootId: string,
    filename: string,
    attackedLines: number
  ) => Promise<void>
) =>
  | ((
      value: string,
      row: IToeLinesData,
      rowIndex: number,
      key: Readonly<IHeaderConfig>
    ) => JSX.Element)
  | undefined = (
  canEdit: boolean,
  handleUpdateAttackedLines: (
    rootId: string,
    filename: string,
    attackedLines: number
  ) => Promise<void>
):
  | ((
      value: string,
      row: IToeLinesData,
      rowIndex: number,
      key: Readonly<IHeaderConfig>
    ) => JSX.Element)
  | undefined => {
  if (!canEdit) {
    return undefined;
  }

  const formatter: (
    value: string,
    row: IToeLinesData,
    rowIndex: number,
    key: Readonly<IHeaderConfig>
  ) => JSX.Element = (
    value: string,
    row: IToeLinesData,
    _rowIndex: number,
    _key: Readonly<IHeaderConfig>
  ): JSX.Element => {
    function handleOnEnter(newValue: number | undefined): void {
      if (!_.isUndefined(newValue)) {
        void handleUpdateAttackedLines(row.rootId, row.filename, newValue);
      }
    }

    return (
      <NumberInput
        defaultValue={_.toNumber(value)}
        max={row.loc}
        min={0}
        onEnter={handleOnEnter}
        tooltipMessage={translate.t(
          "group.toe.lines.formatters.attackedLines.tooltip"
        )}
      />
    );
  };

  return formatter;
};
