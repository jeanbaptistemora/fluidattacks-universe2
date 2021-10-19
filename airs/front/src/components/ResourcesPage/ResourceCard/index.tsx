/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import { CloudImage } from "../../CloudImage";
import {
  ButtonContainer,
  CardContainer,
  CardDescription,
  CardTextContainer,
  CardTitle,
  WebinarLanguage,
} from "../styledComponents";

interface IProps {
  buttonText: string;
  cardType: string;
  description: string;
  image: string;
  language: string;
  title: string;
  urlCard: string;
}

const ResourcesCard: React.FC<IProps> = ({
  buttonText,
  cardType,
  description,
  image,
  language,
  title,
  urlCard,
}: IProps): JSX.Element => (
  <CardContainer className={cardType}>
    <CloudImage alt={language} src={image} styles={"br3 br--top"} />
    <CardTextContainer>
      <div className={"pv3"}>
        <WebinarLanguage>{language}</WebinarLanguage>
      </div>
      <CardTitle>{title}</CardTitle>
      <CardDescription>{description}</CardDescription>
    </CardTextContainer>
    <ButtonContainer>
      <Link
        className={"f5 mt6 hv-fluid-rd fw4 no-underline t-all-5"}
        to={urlCard}
      >
        <button className={"button-white w-80"}>{buttonText}</button>
      </Link>
    </ButtonContainer>
  </CardContainer>
);

export { ResourcesCard };
