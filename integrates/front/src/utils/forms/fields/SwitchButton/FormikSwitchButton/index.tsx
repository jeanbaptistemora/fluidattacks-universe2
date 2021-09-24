import type { FieldProps } from "formik";
import _ from "lodash";
import React from "react";

import type { ISwitchButtonProps } from "components/SwitchButton";
import { SwitchButton } from "components/SwitchButton/index";

declare type FormikSwitchButtonProps = FieldProps & ISwitchButtonProps;

// Custom SwitchButton whose state can be managed by Formik
export const FormikSwitchButton: React.FC<FormikSwitchButtonProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<FormikSwitchButtonProps>
): JSX.Element => {
  const { field, id, disabled, offlabel, onlabel, onChange } = props;
  const { checked } = field;
  // eslint-disable-next-line @typescript-eslint/no-shadow
  function handleOnChange(checked: boolean): void {
    if (!_.isUndefined(onChange)) {
      onChange(checked);
    }
  }

  return (
    <SwitchButton
      checked={checked ?? false}
      disabled={disabled}
      id={id}
      offlabel={offlabel}
      onChange={handleOnChange}
      onlabel={onlabel}
    />
  );
};
