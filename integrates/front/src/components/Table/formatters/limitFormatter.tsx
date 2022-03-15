import React from "react";

import styles from "components/Table/index.css";

export const limitFormatter: (value: string) => JSX.Element = (
  value: string
): JSX.Element => {
  const valueArray: string[] = Array.from(
    new Set(value.split(",").map((element: string): string => element.trim()))
  );
  const additional = valueArray.length - 1;

  return (
    <div>
      <p className={`mb0 ${styles.textMesure} tl truncate`}>
        {valueArray[0]}&nbsp;
        {additional > 0 ? <b>{`+${additional}`}</b> : undefined}
      </p>
    </div>
  );
};
