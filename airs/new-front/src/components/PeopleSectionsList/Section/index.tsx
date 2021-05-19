/* eslint react/forbid-component-props: 0 */
import React from "react";
import ScrollAnimation from "react-animate-on-scroll";

import { CloudImage } from "../../CloudImage";
import {
  LeftColumn,
  RightColumn,
  SectionContainer,
  SectionDescription,
  SectionTitle,
} from "../StyledComponents";

interface IProps {
  description: string;
  imageAlt: string;
  imageSide: string;
  imageSrc: string;
  title: string;
}

const PeopleSection: React.FC<IProps> = ({
  description,
  imageAlt,
  imageSide,
  imageSrc,
  title,
}: IProps): JSX.Element =>
  imageSide === "left" ? (
    <SectionContainer>
      <div>
        <LeftColumn className={"tl-l tc"}>
          <ScrollAnimation animateIn={"animate__fadeInLeft"} animateOnce={true}>
            <CloudImage alt={imageAlt} src={imageSrc} />
          </ScrollAnimation>
        </LeftColumn>
        <RightColumn className={"tl mw6"}>
          <SectionTitle>{title}</SectionTitle>
          <SectionDescription>{description}</SectionDescription>
        </RightColumn>
      </div>
    </SectionContainer>
  ) : (
    <SectionContainer>
      <div>
        <RightColumn className={"tl-l tc"}>
          <ScrollAnimation
            animateIn={"animate__fadeInRight"}
            animateOnce={true}
          >
            <CloudImage alt={imageAlt} src={imageSrc} />
          </ScrollAnimation>
        </RightColumn>
        <LeftColumn className={"tl mw6"}>
          <SectionTitle>{title}</SectionTitle>
          <SectionDescription>{description}</SectionDescription>
        </LeftColumn>
      </div>
    </SectionContainer>
  );

export { PeopleSection };
