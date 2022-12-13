import React, { useCallback } from "react";

import { Container } from "../../Container";
import { Text } from "../../Typography";
import { StyledInput } from "../styledComponents";
import type { IInputProps } from "../types";

const Date: React.FC<IInputProps> = ({ label = "", onChange }): JSX.Element => {
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
      <StyledInput min={"2017-01-01"} onChange={onChangeEvent} type={"date"} />
    </Container>
  );
};

export { Date };
