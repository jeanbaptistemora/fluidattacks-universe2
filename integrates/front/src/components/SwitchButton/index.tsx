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
  offlabel: string;
  onChange?: (checked: boolean) => void;
  onlabel: string;
}

export const SwitchButton: React.FC<ISwitchButtonProps> = (
  props: Readonly<ISwitchButtonProps>
): JSX.Element => {
  const {
    checked,
    disabled = false,
    offlabel,
    onChange = undefined,
    onlabel,
  } = props;

  function handleClick(): void {
    if (onChange) {
      onChange(!checked);
    }
  }

  return (
    <Switch
      onClick={disabled ? undefined : handleClick}
      theme={{ on: checked }}
    >
      <SwitchGroup theme={{ on: checked }}>
        <SwitchOn>{onlabel}</SwitchOn>
        <SwitchOff>{offlabel}</SwitchOff>
        <SwitchHandle />
      </SwitchGroup>
    </Switch>
  );
};
