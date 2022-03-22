import React, { useCallback } from "react";

import { Container, Slider } from "./styles";

interface ISwitchProps {
  checked: boolean;
  disabled?: boolean;
  name?: string;
  onChange: React.ChangeEventHandler<HTMLInputElement>;
}

const Switch: React.FC<ISwitchProps> = ({
  checked,
  disabled,
  name,
  onChange,
}: Readonly<ISwitchProps>): JSX.Element => {
  // Disable click propagation in favor of the input onChange event
  const handleClick = useCallback(
    (event: React.MouseEvent<HTMLLabelElement>): void => {
      event.stopPropagation();
    },
    []
  );

  return (
    <Container onClick={handleClick}>
      <input
        aria-label={name}
        checked={checked}
        disabled={disabled}
        name={name}
        onChange={onChange}
        type={"checkbox"}
      />
      <Slider />
    </Container>
  );
};

export { ISwitchProps, Switch };
