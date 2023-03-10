/* eslint @typescript-eslint/no-unsafe-member-access: 0*/
/* eslint @typescript-eslint/no-unsafe-call: 0*/
/* eslint @typescript-eslint/no-explicit-any: 0*/
import React, { Fragment, createElement } from "react";
import rehypeReact from "rehype-react";

import { BlogCta } from "./components/BlogCta";
import { BlogLink } from "./components/BlogLink";
import { Caution } from "./components/Caution";
import { Header2 } from "./components/Header2";
import { Header3 } from "./components/Header3";
import { Header4 } from "./components/Header4";
import { ImageBlock } from "./components/ImageBlock";
import { Paragraph } from "./components/Paragraph";
import { Quote } from "./components/Quote";
import { TableBlock } from "./components/TableBlock";
import { VideoBlock } from "./components/VideoBlock";
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
      "caution-box": Caution,
      "cta-banner": BlogCta,
      h2: Header2,
      h3: Header3,
      h4: Header4,
      "image-block": ImageBlock,
      p: Paragraph,
      "quote-box": Quote,
      "table-block": TableBlock,
      "video-block": VideoBlock,
    },
    createElement,
    options: {
      fragment: Fragment,
    },
  }).Compiler;

  return (
    <Container ph={4} pv={5}>
      <Container
        center={true}
        direction={"reverse"}
        display={"flex"}
        maxWidth={"1440px"}
        wrap={"wrap"}
      >
        <Container width={"95%"} widthMd={"85%"} widthSm={"100%"}>
          <Container center={true} maxWidth={"800px"}>
            <div className={"new-internal"}>{renderAst(htmlAst)}</div>
          </Container>
        </Container>
        <Container width={"5%"} widthMd={"15%"} widthSm={"100%"}>
          <ShareSection slug={slug} />
        </Container>
      </Container>
    </Container>
  );
};

export { ContentSection };
