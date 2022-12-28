/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/no-autofocus */
import _ from "lodash";
import React from "react";

import type { IToeLinesData } from "../types";
import { NumberInput } from "components/NumberInput";
import { translate } from "utils/translations/translate";

export const editableAttackedLinesFormatter = (
  canEdit: boolean,
  handleUpdateAttackedLines: (
    rootId: string,
    filename: string,
    attackedLines: number
  ) => Promise<void>,
  row: IToeLinesData
): JSX.Element | string => {
  if (!canEdit) {
    return String(row.attackedLines);
  }
  const value = row.attackedLines;

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
