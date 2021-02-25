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
  id?: string;
  offlabel: string;
  onChange?: (checked: boolean) => void;
  onlabel: string;
}

const SwitchButton: React.FC<ISwitchButtonProps> = (
  props: Readonly<ISwitchButtonProps>
): JSX.Element => {
  const {
    checked,
    disabled = false,
    id,
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
      id={id}
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

export { SwitchButton, ISwitchButtonProps };
