/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/no-autofocus */
import _ from "lodash";
import React, { useState } from "react";

import type { IToeLinesData } from "../types";
import type { IHeaderConfig } from "components/Table/types";
import { StyledInput } from "utils/forms/fields/styles";

interface IEditableFormatterProps {
  defaultValue: string;
  row: IToeLinesData;
  handleUpdateAttackedLines: (
    rootId: string,
    filename: string,
    attackedLines: number
  ) => Promise<void>;
}

const EditableFormatter: React.FC<IEditableFormatterProps> = ({
  defaultValue,
  row,
  handleUpdateAttackedLines,
}): JSX.Element => {
  const [isFocused, setIsFocused] = useState(false);

  function handleOnDivClick(_event: React.MouseEvent<HTMLDivElement>): void {
    setIsFocused(true);
  }

  function handleOnInputBlur(event: React.FocusEvent<HTMLInputElement>): void {
    setIsFocused(false);
    event.stopPropagation();
  }

  async function handleOnInputKeyUp(
    event: React.KeyboardEvent<HTMLInputElement>
  ): Promise<void> {
    event.stopPropagation();
    if (event.key === "Enter") {
      await handleUpdateAttackedLines(
        row.rootId,
        row.filename,
        _.toNumber(event.currentTarget.value)
      );
      setIsFocused(false);
    }
  }

  return isFocused ? (
    <StyledInput
      autoFocus={true}
      defaultValue={defaultValue}
      onBlur={handleOnInputBlur}
      onKeyUp={handleOnInputKeyUp}
      type={"number"}
    />
  ) : (
    <div
      aria-checked={false}
      onClick={handleOnDivClick}
      role={"switch"}
      tabIndex={0}
    >
      {defaultValue}
    </div>
  );
};

export const editableAttackedLinesFormatter: (
  handleUpdateAttackedLines: (
    rootId: string,
    filename: string,
    attackedLines: number
  ) => Promise<void>
) => (
  value: string,
  row: IToeLinesData,
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
  row: IToeLinesData,
  rowIndex: number,
  key: Readonly<IHeaderConfig>
) => JSX.Element) => {
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
    return (
      <EditableFormatter
        defaultValue={value}
        handleUpdateAttackedLines={handleUpdateAttackedLines}
        row={row}
      />
    );
  };

  return formatter;
};
