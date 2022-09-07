/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint react/forbid-component-props: 0 */
import React from "react";
import { AnimationOnScroll } from "react-animation-on-scroll";

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
          <AnimationOnScroll
            animateIn={"animate__fadeInLeft"}
            animateOnce={true}
          >
            <CloudImage alt={imageAlt} src={imageSrc} />
          </AnimationOnScroll>
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
          <AnimationOnScroll
            animateIn={"animate__fadeInRight"}
            animateOnce={true}
          >
            <CloudImage alt={imageAlt} src={imageSrc} />
          </AnimationOnScroll>
        </RightColumn>
        <LeftColumn className={"tl mw6"}>
          <SectionTitle>{title}</SectionTitle>
          <SectionDescription>{description}</SectionDescription>
        </LeftColumn>
      </div>
    </SectionContainer>
  );

export { PeopleSection };
