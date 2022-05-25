/* eslint react/forbid-component-props: 0 */
import React from "react";

import { CloudImage } from "../../../CloudImage";
import { Paragraph } from "../../../Texts";
import { CardContainer } from "../styledComponents";
import type { IProductCard } from "../types";

const ProductCard: React.FC<IProductCard> = ({
  image,
  text,
}: IProductCard): JSX.Element => {
  return (
    <CardContainer>
      <CloudImage
        alt={`card-image-${image}`}
        src={`airs/product-overview/cards-section/${image}`}
        styles={"mt4"}
      />
      <Paragraph
        fColor={"#5c5c70"}
        fSize={"24"}
        marginBottom={"2"}
        marginTop={"2"}
        maxWidth={"330"}
      >
        {text}
      </Paragraph>
    </CardContainer>
  );
};

export { ProductCard };
