/* eslint-disable react/forbid-component-props
  --------
  We need className to override default styles from react-bootstrap.
*/
import React from "react";
import { translate } from "utils/translations/translate";

export const limitFormatter: (value: string) => JSX.Element = (
  value: string
): JSX.Element => {
  const linesLimit: number = 15;
  const valueArray: string[] = value
    .split(",")
    .map((element: string): string => element.trim());
  const newValue: string = valueArray.slice(0, linesLimit).join(", ");

  return (
    <div>
      <p>{newValue}</p>
      {valueArray.length > linesLimit && (
        <p>{translate.t("dataTableNext.more")}</p>
      )}
    </div>
  );
};
