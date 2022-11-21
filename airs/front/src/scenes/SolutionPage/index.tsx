/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { HeaderSection } from "./HeaderSection";
import { MainSection } from "./MainSection";

import { Container } from "../../components/Container";
import { CtaBanner } from "../../components/CtaBanner";

interface ISolutionPageProps {
  description: string;
  htmlAst: string;
  identifier: string;
  image: string;
  title: string;
}

const SolutionPage: React.FC<ISolutionPageProps> = ({
  description,
  htmlAst,
  identifier,
  image,
  title,
}): JSX.Element => {
  const ctaParagraph =
    `This culture is gaining strength as an increasing number of organizations are ` +
    `building more secure software day by day. Don't miss out on the benefits, ` +
    `and ask us about our 21-day free trial for a taste of our ${identifier} solution.`;

  return (
    <React.Fragment>
      <HeaderSection description={description} image={image} title={title} />
      <MainSection htmlAst={htmlAst} />
      <Container bgColor={"#fff"} ph={4} pv={5}>
        <CtaBanner
          button1Link={"/free-trial/"}
          button1Text={"Start free trial"}
          button2Link={"/contact-us/"}
          button2Text={"Contact now"}
          image={"/airs/solutions/cta-banner"}
          matomoAction={"Solution"}
          paragraph={ctaParagraph}
          title={`Get Started with Fluid Attacks' ${identifier} rigth now`}
        />
      </Container>
    </React.Fragment>
  );
};

export { SolutionPage };
