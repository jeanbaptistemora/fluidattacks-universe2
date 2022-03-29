/* eslint react/forbid-component-props: 0 */
import React from "react";

import { CloudImage } from "../../../CloudImage";
import { CardContainer, CardText, CardTitle } from "../styledComponents";
import type { IProductCard } from "../types";

const ProductCard: React.FC<IProductCard> = ({
  image,
  text,
  title,
}: IProductCard): JSX.Element => {
  return (
    <CardContainer>
      <CloudImage
        alt={`card-image-${image}`}
        src={`airs/product-overview/cards-section/${image}`}
        styles={""}
      />
      <CardTitle>{title}</CardTitle>
      <CardText>{text}</CardText>
    </CardContainer>
  );
};

export { ProductCard };
