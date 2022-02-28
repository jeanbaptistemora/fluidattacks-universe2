/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import { CloudImage } from "../../../CloudImage";

interface IProps {
  image: string;
  url: string;
}

const ResourceCard: React.FC<IProps> = ({
  image,
  url,
}: IProps): JSX.Element => (
  <Link to={`${url}`}>
    <CloudImage
      alt={image}
      src={`/airs/home/${image}`}
      styles={"ma3 resources-card-animation t-all-3-eio"}
    />
  </Link>
);

export { ResourceCard };
