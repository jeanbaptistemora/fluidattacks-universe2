/* eslint-disable jsx-a11y/no-autofocus */
import _ from "lodash";
import React from "react";

import type { IHeaderConfig } from "components/Table/types";
import { StyledInput } from "utils/forms/fields/styles";

export const editableAttackedLinesFormatter: (
  handleUpdateAttackedLines: (
    rootId: string,
    filename: string,
    attackedLines: number
  ) => Promise<void>
) => (
  value: string,
  row: Readonly<Record<string, string>>,
  rowIndex: number,
  key: Readonly<IHeaderConfig>
) => JSX.Element = (
  handleUpdateAttackedLines: (
    rootId: string,
    filename: string,
    attackedLines: number
  ) => Promise<void>
): ((
  value: string,
  row: Readonly<Record<string, string>>,
  rowIndex: number,
  key: Readonly<IHeaderConfig>
) => JSX.Element) => {
  const formatter: (
    value: string,
    row: Readonly<Record<string, string>>,
    rowIndex: number,
    key: Readonly<IHeaderConfig>
  ) => JSX.Element = (
    value: string,
    row: Readonly<Record<string, string>>,
    _rowIndex: number,
    _key: Readonly<IHeaderConfig>
  ): JSX.Element => {
    function handleOnBlur(event: React.FocusEvent<HTMLInputElement>): void {
      event.stopPropagation();
    }

    function handleOnKeyUp(event: React.KeyboardEvent<HTMLInputElement>): void {
      event.stopPropagation();
      if (event.key === "Enter") {
        void handleUpdateAttackedLines(
          row.rootId,
          row.filename,
          _.toNumber(event.currentTarget.value)
        );
      }
    }

    return (
      <StyledInput
        autoFocus={true}
        defaultValue={value}
        onBlur={handleOnBlur}
        onKeyUp={handleOnKeyUp}
        type={"number"}
      />
    );
  };

  return formatter;
};
