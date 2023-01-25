import { faXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC, MouseEventHandler } from "react";
import React from "react";

import { CloseButton } from "./styles";

import { Container } from "components/Container";
import { Text } from "components/Text";

interface ICloseTagProps {
  text: string;
  onClose: MouseEventHandler<HTMLButtonElement>;
}

const CloseTag: FC<ICloseTagProps> = ({ text, onClose }): JSX.Element => {
  return (
    <Container display={"inline-block"}>
      <Container
        align={"center"}
        bgColor={"#d2d2da"}
        br={"3px"}
        display={"flex"}
        pb={"4px"}
        pl={"4px"}
        pr={"4px"}
        pt={"4px"}
      >
        <Text disp={"inline-block"} size={"small"}>
          {text}
        </Text>
        <CloseButton onClick={onClose}>
          <FontAwesomeIcon icon={faXmark} />
        </CloseButton>
      </Container>
    </Container>
  );
};

export type { ICloseTagProps };
export { CloseTag };
