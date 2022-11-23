import React from "react";

import { CloudImage } from "../../CloudImage";
import { Col, Text, TextContainer } from "../styledComponents";

interface IProps {
  date: string;
  text: string;
}

const TimeItem: React.FC<IProps> = ({ date, text }: IProps): JSX.Element => (
  <Col>
    <CloudImage
      alt={"Time-lapse-logo"}
      src={"/airs/icons/red-circle-check"}
      styles={"time-lapse-icon mt3 mr2"}
    />
    <TextContainer>
      <Text>{date}</Text>
      <Text>{text}</Text>
    </TextContainer>
  </Col>
);

export { TimeItem };
