import _ from "lodash";
import React from "react";

import type { ISwitchButtonProps } from "components/SwitchButton";
import { SwitchButton } from "components/SwitchButton/index";

export interface IFormSwitchButtonProps extends ISwitchButtonProps {
  input: {
    checked: boolean;
    onChange: (checked: boolean) => void;
  };
}

// Custom SwitchButton whose state can be managed by redux-form
export const FormSwitchButton: React.FC<IFormSwitchButtonProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<IFormSwitchButtonProps>
): JSX.Element => {
  const { input, id, disabled, offlabel, onlabel, onChange } = props;
  const { onChange: reduxFormOnChange, checked: reduxFormChecked } = input;

  function handleOnChange(checked: boolean): void {
    reduxFormOnChange(checked);
    if (!_.isUndefined(onChange)) {
      onChange(checked);
    }
  }

  return (
    <SwitchButton
      checked={reduxFormChecked}
      disabled={disabled}
      id={id}
      offlabel={offlabel}
      onChange={handleOnChange}
      onlabel={onlabel}
    />
  );
};
