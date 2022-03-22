import React from "react";

import { Container, Slider } from "./styles";

interface ISwitchProps {
  checked: boolean;
  onChange: React.ChangeEventHandler<HTMLInputElement>;
}

const Switch: React.FC<ISwitchProps> = ({
  checked,
  onChange,
}: ISwitchProps): JSX.Element => {
  return (
    <Container>
      <input checked={checked} onChange={onChange} type={"checkbox"} />
      <Slider />
    </Container>
  );
};

export { ISwitchProps, Switch };
