import React from "react";

import styles from "components/DataTableNext/index.css";
import { translate } from "utils/translations/translate";

export const limitFormatter: (value: string) => JSX.Element = (
  value: string
): JSX.Element => {
  const linesLimit: number = 15;
  const valueArray: string[] = Array.from(
    new Set(value.split(",").map((element: string): string => element.trim()))
  );

  return (
    <div>
      {valueArray.slice(0, linesLimit).map(
        (formatValue: string, index: number): JSX.Element => (
          <p
            className={`mb0 ${styles.textMesure} tl truncate`}
            key={index.toString()}
          >
            {formatValue}
          </p>
        )
      )}
      {valueArray.length > linesLimit && (
        <p>{translate.t("dataTableNext.more")}</p>
      )}
    </div>
  );
};
