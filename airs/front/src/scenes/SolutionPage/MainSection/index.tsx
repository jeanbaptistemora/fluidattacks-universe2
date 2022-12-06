/* eslint @typescript-eslint/no-unsafe-member-access: 0*/
/* eslint @typescript-eslint/no-unsafe-call: 0*/
/* eslint @typescript-eslint/no-explicit-any: 0*/
import React, { createElement } from "react";
import rehypeReact from "rehype-react";

import { FaqContainer } from "./components/FaqContainer";
import { GridContainer } from "./components/GridContainer";
import { Header2 } from "./components/Header2";
import { Paragraph } from "./components/Paragraph";
import { SolutionCard } from "./components/SolutionCard";
import { SolutionCtaBanner } from "./components/SolutionCtaBanner";
import { SolutionFaq } from "./components/SolutionFaq";
import { SolutionSlideShow } from "./components/SolutionSlideShow";
import { TextContainer } from "./components/TextContainer";

import { Container } from "../../../components/Container";

interface IMainProps {
  htmlAst: string;
}

const MainSection: React.FC<IMainProps> = ({ htmlAst }): JSX.Element => {
  const renderAst = new (rehypeReact as any)({
    components: {
      "faq-container": FaqContainer,
      "grid-container": GridContainer,
      h2: Header2,
      p: Paragraph,
      "solution-card": SolutionCard,
      "solution-cta": SolutionCtaBanner,
      "solution-faq": SolutionFaq,
      "solution-slide": SolutionSlideShow,
      "text-container": TextContainer,
    },
    createElement,
  }).Compiler;

  return <Container bgColor={"#fff"}>{renderAst(htmlAst)}</Container>;
};

export { MainSection };
