import BootstrapSwitchButton from "bootstrap-switch-button-react";
import React from "react";
import _ from "lodash";

export interface ISwitchButtonProps
  extends React.ComponentProps<typeof BootstrapSwitchButton> {
  input: {
    checked: boolean;
    onChange: (checked: boolean) => void;
  };
}

// Custom BootstrapSwitchButton whose state can be managed by redux-form
export const SwitchButton: React.FC<ISwitchButtonProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<ISwitchButtonProps>
): JSX.Element => {
  const {
    input,
    disabled,
    offlabel,
    onlabel,
    onstyle,
    style,
    onChange,
  } = props;
  const { onChange: reduxFormOnChange, checked: reduxFormChecked } = input;

  function handleOnChange(checked: boolean): void {
    reduxFormOnChange(checked);
    if (!_.isUndefined(onChange)) {
      onChange(checked);
    }
  }

  return (
    <BootstrapSwitchButton
      checked={reduxFormChecked}
      disabled={disabled}
      offlabel={offlabel}
      onChange={handleOnChange}
      onlabel={onlabel}
      onstyle={onstyle}
      // We need it to override default styles from bootstrap-switch-button.
      // eslint-disable-next-line react/forbid-component-props
      style={style}
    />
  );
};
