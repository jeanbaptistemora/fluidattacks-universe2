/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import React from "react";

import {
  Switch,
  SwitchGroup,
  SwitchHandle,
  SwitchOff,
  SwitchOn,
} from "styles/styledComponents";

interface ISwitchButtonProps {
  checked: boolean;
  disabled?: boolean;
  fontSize?: string;
  id?: string;
  offlabel: string;
  onChange?: (checked: boolean) => void;
  onlabel: string;
  switchColor?: string;
}

const SwitchButton: React.FC<ISwitchButtonProps> = (
  props: Readonly<ISwitchButtonProps>
): JSX.Element => {
  const {
    checked,
    disabled = false,
    fontSize,
    id,
    offlabel,
    onChange = undefined,
    onlabel,
    switchColor = "bg-switch b--switch",
  } = props;

  function handleClick(): void {
    if (onChange) {
      onChange(!checked);
    }
  }

  return (
    <Switch
      className={fontSize}
      id={id}
      onClick={disabled ? undefined : handleClick}
      theme={{ color: switchColor, on: checked }}
    >
      <SwitchGroup theme={{ on: checked }}>
        <SwitchOn className={switchColor}>{onlabel}</SwitchOn>
        <SwitchOff>{offlabel}</SwitchOff>
        <SwitchHandle />
      </SwitchGroup>
    </Switch>
  );
};

export { SwitchButton, ISwitchButtonProps };
