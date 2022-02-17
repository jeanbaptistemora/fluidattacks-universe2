import { Field } from "formik";
import React from "react";

import type { IHeaderConfig } from "components/DataTableNext/types";
import { FormikCheckbox } from "utils/forms/fields";

export const changeVulnReattackHoldFormatter = (
  _value: string,
  row: Readonly<Record<string, string>>,
  rowIndex: number,
  key: Readonly<IHeaderConfig>
): JSX.Element => {
  function handleOnChange(): void {
    if (key.changeFunction !== undefined) {
      key.changeFunction(row);
    }
  }

  return (
    <Field
      component={FormikCheckbox}
      label={""}
      name={`${rowIndex}`}
      onChange={handleOnChange}
      type={"checkbox"}
      value={row.affected}
    />
  );
};
