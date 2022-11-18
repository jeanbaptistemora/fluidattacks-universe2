/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint @typescript-eslint/no-unsafe-member-access: 0*/
/* eslint @typescript-eslint/no-unsafe-call: 0*/
/* eslint @typescript-eslint/no-explicit-any: 0*/
import React, { createElement } from "react";
import rehypeReact from "rehype-react";

import { GridContainer } from "./components/GridContainer";
import { Header2 } from "./components/Header2";
import { Paragraph } from "./components/Paragraph";
import { SolutionCard } from "./components/SolutionCard";
import { SolutionSlideShow } from "./components/SolutionSlideShow";
import { TextContainer } from "./components/TextContainer";

import { Container } from "../../../components/Container";

interface IMainProps {
  htmlAst: string;
}

const MainSection: React.FC<IMainProps> = ({ htmlAst }): JSX.Element => {
  const renderAst = new (rehypeReact as any)({
    components: {
      "grid-container": GridContainer,
      h2: Header2,
      p: Paragraph,
      "solution-card": SolutionCard,
      "solution-slide": SolutionSlideShow,
      "text-container": TextContainer,
    },
    createElement,
  }).Compiler;

  return (
    <Container bgColor={"#fff"} pv={5}>
      {renderAst(htmlAst)}
    </Container>
  );
};

export { MainSection };
