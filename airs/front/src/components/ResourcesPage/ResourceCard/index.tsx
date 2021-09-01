/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import { RegularRedButton } from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";
import {
  ButtonContainer,
  CardContainer,
  CardDescription,
  CardTextContainer,
  CardTitle,
  WebinarImageContainer,
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
    {cardType === "webinar-card" ? (
      <WebinarImageContainer className={image}>
        <CloudImage alt={language} src={image} styles={"br3 br--top"} />
        <div className={"pa3 top-0 absolute"}>
          <WebinarLanguage>{language}</WebinarLanguage>
        </div>
      </WebinarImageContainer>
    ) : (
      <CloudImage alt={language} src={image} styles={"br3 br--top"} />
    )}
    <CardTextContainer>
      <CardTitle>{title}</CardTitle>
      <CardDescription>{description}</CardDescription>
    </CardTextContainer>
    <ButtonContainer>
      <Link to={urlCard}>
        <RegularRedButton>{buttonText}</RegularRedButton>
      </Link>
    </ButtonContainer>
  </CardContainer>
);

export { ResourcesCard };
