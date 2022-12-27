/* eslint @typescript-eslint/no-unsafe-member-access: 0*/
/* eslint @typescript-eslint/no-unsafe-call: 0*/
/* eslint @typescript-eslint/no-explicit-any: 0*/
import React, { createElement } from "react";
import rehypeReact from "rehype-react";

import { BlogLink } from "./components/BlogLink";
import { Header2 } from "./components/Header2";
import { Header3 } from "./components/Header3";
import { Header4 } from "./components/Header4";
import { ImageBlock } from "./components/ImageBlock";
import { Paragraph } from "./components/Paragraph";
import { TableBlock } from "./components/TableBlock";
import { ShareSection } from "./ShareSection";

import { Container } from "../../../components/Container";

interface IContentProps {
  htmlAst: string;
  slug: string;
}

const ContentSection: React.FC<IContentProps> = ({
  htmlAst,
  slug,
}): JSX.Element => {
  const renderAst = new (rehypeReact as any)({
    components: {
      a: BlogLink,
      h2: Header2,
      h3: Header3,
      h4: Header4,
      "image-block": ImageBlock,
      p: Paragraph,
      "table-block": TableBlock,
    },
    createElement,
  }).Compiler;

  return (
    <Container ph={4} pv={5}>
      <Container
        center={true}
        display={"flex"}
        maxWidth={"1440px"}
        wrap={"wrap"}
      >
        <Container width={"15%"} widthSm={"100%"}>
          <ShareSection slug={slug} />
        </Container>
        <Container width={"85%"} widthSm={"100%"}>
          <Container center={true} maxWidth={"1000px"}>
            <div className={"new-internal"}>{renderAst(htmlAst)}</div>
          </Container>
        </Container>
      </Container>
    </Container>
  );
};

export { ContentSection };