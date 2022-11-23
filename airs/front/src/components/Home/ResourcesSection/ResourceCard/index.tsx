import React from "react";

import { AirsLink } from "../../../AirsLink";
import { CloudImage } from "../../../CloudImage";

interface IProps {
  image: string;
  url: string;
}

const ResourceCard: React.FC<IProps> = ({
  image,
  url,
}: IProps): JSX.Element => (
  <AirsLink href={`${url}`}>
    <CloudImage
      alt={image}
      src={`/airs/home/${image}`}
      styles={"ma3 resource-home-card resources-card-animation t-all-3-eio"}
    />
  </AirsLink>
);

export { ResourceCard };
