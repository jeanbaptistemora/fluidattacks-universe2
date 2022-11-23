import React from "react";

import { SimpleCard } from "../../../../components/SimpleCard";
import type { ISimpleCardProps } from "../../../../components/SimpleCard/types";

const SolutionCard: React.FC<ISimpleCardProps> = ({
  description,
  image,
  title,
}): JSX.Element => (
  <SimpleCard
    description={description}
    descriptionColor={"#535365"}
    image={image}
    title={title}
    titleColor={"#2e2e38"}
    titleMinHeight={"64px"}
    width={"464px"}
    widthSm={"100%"}
  />
);

export { SolutionCard };
