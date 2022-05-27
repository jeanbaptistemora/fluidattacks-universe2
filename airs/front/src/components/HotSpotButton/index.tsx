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
    <React.Fragment>
      <ButtonContainer
        data-background-color={"black"}
        data-class={"roboto"}
        data-effect={"solid"}
        data-for={id}
        data-tip={tooltipMessage}
        isRight={isRight}
        onClick={onClick}
      >
        <FirstCircle />
        <SecondCircle />
        <ThirdCircle />
      </ButtonContainer>
      <ReactTooltip id={id} />
    </React.Fragment>
  );
};

export { HotSpotButton };
