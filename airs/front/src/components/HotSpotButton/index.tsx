/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
        data-class={"poppins"}
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
