import { faCircle, faCircleCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import type { IProgressBarProps } from "./styles";
import { Container, ProgressBar, StepsContainer } from "./styles";

interface IProgressIndicatorProps extends IProgressBarProps {
  showSteps?: boolean;
}

const ProgressIndicator: React.FC<IProgressIndicatorProps> = ({
  max = 5,
  showSteps = true,
  value = 1,
}: Readonly<IProgressIndicatorProps>): JSX.Element => {
  return (
    <Container>
      <ProgressBar max={max} value={Math.min(Math.max(value, 0), max)} />
      {showSteps ? (
        <StepsContainer>
          <FontAwesomeIcon icon={faCircle} />
          {Array.from(
            Array(value),
            (el: number): JSX.Element => (
              <FontAwesomeIcon icon={faCircleCheck} key={`y${el}`} />
            )
          )}
          {Array.from(
            Array(max - value),
            (el: number): JSX.Element => (
              <FontAwesomeIcon
                color={"#b0b0bf"}
                icon={faCircle}
                key={`n${el}`}
              />
            )
          )}
        </StepsContainer>
      ) : undefined}
    </Container>
  );
};

export type { IProgressIndicatorProps };
export { ProgressIndicator };
