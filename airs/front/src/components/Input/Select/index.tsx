import React, { useCallback } from "react";

import { StyledOption, StyledSelect } from "./styledComponents";
import type { ISelectProps } from "./types";

import { capitalizeDashedString, stringToUri } from "../../../utils/utilities";
import { Container } from "../../Container";
import { Text } from "../../Typography";

const Select: React.FC<ISelectProps> = ({
  label = "",
  onChange,
  options,
}): JSX.Element => {
  const onChangeEvent = useCallback(
    (event: React.ChangeEvent<HTMLSelectElement>): void => {
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
      <StyledSelect onChange={onChangeEvent}>
        <StyledOption value={"All"}>{"All"}</StyledOption>
        {options.map((option): JSX.Element => {
          return (
            <StyledOption key={option} value={option}>
              {capitalizeDashedString(stringToUri(option))}
            </StyledOption>
          );
        })}
      </StyledSelect>
    </Container>
  );
};

export { Select };
