import {
  faCircleCheck,
  faCircleXmark,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";

import type { ILabelProps } from "./styles";
import { Floating, Input, Label } from "./styles";

interface IToggleProps extends Partial<ILabelProps> {
  initChecked?: boolean;
  name?: string;
  onChange: (value: boolean) => void;
}

const Toggle: React.FC<IToggleProps> = ({
  initChecked = false,
  name,
  onChange,
  size = 24,
}: Readonly<IToggleProps>): JSX.Element => {
  const [checked, setChecked] = useState(initChecked);
  const onToggle = useCallback((): void => {
    setChecked(!checked);
    onChange(checked);
  }, [checked, onChange]);

  return (
    <Label size={size}>
      <Input
        checked={checked}
        name={name}
        onChange={onToggle}
        type={"checkbox"}
      />
      <Floating side={checked ? "left" : "right"}>
        <FontAwesomeIcon icon={checked ? faCircleCheck : faCircleXmark} />
      </Floating>
    </Label>
  );
};

export type { IToggleProps };
export { Toggle };
