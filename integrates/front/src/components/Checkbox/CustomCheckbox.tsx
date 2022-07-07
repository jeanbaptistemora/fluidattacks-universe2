import { faCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useState } from "react";

import type { ICheckboxLabelProps } from "./styles";
import { CheckboxInput, CheckboxLabel } from "./styles";

interface ICheckboxProps extends ICheckboxLabelProps {
  id?: string;
  initChecked?: boolean;
  name?: string;
  onChange: (value: boolean) => void;
}

const CustomCheckbox: React.FC<ICheckboxProps> = ({
  disabled,
  id,
  initChecked = false,
  name,
  onChange,
}: Readonly<ICheckboxProps>): JSX.Element => {
  const [checked, setChecked] = useState(initChecked);
  const onToggle = useCallback((): void => {
    setChecked(!checked);
    onChange(checked);
  }, [checked, onChange]);

  return (
    <CheckboxLabel disabled={disabled} htmlFor={id}>
      <CheckboxInput
        disabled={disabled}
        id={id}
        name={name}
        onChange={onToggle}
      />
      {checked ? <FontAwesomeIcon icon={faCheck} /> : undefined}
    </CheckboxLabel>
  );
};

export type { ICheckboxProps };
export { CustomCheckbox };
