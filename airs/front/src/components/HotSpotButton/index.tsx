import React from "react";
import ReactTooltip from "react-tooltip";

import {
  ButtonContainer,
  FirstCircle,
  SecondCircle,
  ThirdCircle,
} from "./styledComponents";

interface IHotspotButton {
  id: string;
  isRight: boolean;
  onClick: () => void;
  tooltipMessage: string;
}

const HotSpotButton: React.FC<IHotspotButton> = ({
  id,
  isRight,
  onClick,
  tooltipMessage,
}: IHotspotButton): JSX.Element => {
  return (
    <ButtonContainer
      data-for={id}
      data-tip={tooltipMessage}
      data-type={"dark"}
      isRight={isRight}
      onClick={onClick}
    >
      <FirstCircle />
      <SecondCircle />
      <ThirdCircle />
      <ReactTooltip id={id} />
    </ButtonContainer>
  );
};

export { HotSpotButton };
