/* eslint react/forbid-component-props: 0 */
import React from "react";

import { AirsLink } from "../../AirsLink";
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
      <AirsLink href={urlCard}>
        <button
          className={
            "button-white w-80 f5 hv-fluid-rd fw4 no-underline t-all-5"
          }
        >
          {buttonText}
        </button>
      </AirsLink>
    </ButtonContainer>
  </CardContainer>
);

export { ResourcesCard };
