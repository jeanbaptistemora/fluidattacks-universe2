/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import { PhantomRegularRedButton } from "../../../../styles/styledComponents";
import { CloudImage } from "../../../CloudImage";
import {
  CardContainer,
  CardDescription,
  CardTextContainer,
  CardTitle,
} from "../styledComponents";

interface IProps {
  description: string;
  image: string;
  title: string;
  urlCard: string;
}

const SolutionCard: React.FC<IProps> = ({
  description,
  image,
  title,
  urlCard,
}: IProps): JSX.Element => (
  <CardContainer>
    <CloudImage alt={image} src={`/airs/home/${image}`} />
    <CardTextContainer>
      <CardTitle>{title}</CardTitle>
      <CardDescription>{description}</CardDescription>
      <Link className={"no-underline"} to={urlCard}>
        <PhantomRegularRedButton className={"mb4"}>
          {"Go to solution"}
        </PhantomRegularRedButton>
      </Link>
    </CardTextContainer>
  </CardContainer>
);

export { SolutionCard };
