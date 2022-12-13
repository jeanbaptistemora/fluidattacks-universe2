import React, { useCallback } from "react";

import { Container } from "../../Container";
import { Text } from "../../Typography";
import { StyledInput } from "../styledComponents";
import type { IInputProps } from "../types";

const TextArea: React.FC<IInputProps> = ({
  label = "",
  onChange,
  placeHolder = "",
}): JSX.Element => {
  const onChangeEvent = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      onChange(event.target.value);
    },
    [onChange]
  );

  return (
    <Container>
      {label ? (
        <Text color={"#2e2e38"} size={"small"}>
          {label}
        </Text>
      ) : undefined}
      <StyledInput
        bgColor={"#f4f4f6"}
        borderColor={"#f4f4f6"}
        onChange={onChangeEvent}
        placeholder={placeHolder}
        type={"text"}
      />
    </Container>
  );
};

export { TextArea };
