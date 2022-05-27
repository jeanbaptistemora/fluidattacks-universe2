import React from "react";

import {
  ButtonContainer,
  FirstCircle,
  SecondCircle,
  ThirdCircle,
} from "./styledComponents";

interface IHotspotButton {
  isRight: boolean;
  onClick: () => void;
}

const HotSpotButton: React.FC<IHotspotButton> = ({
  isRight,
  onClick,
}: IHotspotButton): JSX.Element => {
  return (
    <ButtonContainer isRight={isRight} onClick={onClick}>
      <FirstCircle />
      <SecondCircle />
      <ThirdCircle />
    </ButtonContainer>
  );
};

export { HotSpotButton };
