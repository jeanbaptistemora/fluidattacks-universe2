/* eslint react/forbid-component-props: 0 */
import React from "react";

import { CloudImage } from "../../../CloudImage";
import { CardContainer, CardText, CardTitle } from "../styledComponents";
import type { INumberCard } from "../types";

const NumberCard: React.FC<INumberCard> = ({
  hasTitle,
  image,
  isGray,
  text,
  title,
  typeIcon,
}: INumberCard): JSX.Element => {
  return (
    <CardContainer>
      <CloudImage
        alt={`card-image-${image}`}
        src={`airs/home/${image}`}
        styles={typeIcon === "1" ? "number-card-icon" : "number-card-icon-2"}
      />
      {hasTitle ? <CardTitle>{title}</CardTitle> : undefined}
      <CardText gray={isGray}>{text}</CardText>
    </CardContainer>
  );
};

// eslint-disable-next-line fp/no-mutation
NumberCard.defaultProps = {
  title: "",
};

export { NumberCard };
