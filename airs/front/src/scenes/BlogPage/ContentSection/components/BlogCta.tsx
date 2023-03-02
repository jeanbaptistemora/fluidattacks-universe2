import React from "react";

import { Container } from "../../../../components/Container";
import { CtaBanner } from "../../../../components/CtaBanner";

interface IBlogCta {
  buttontxt: string;
  link: string;
  title: string;
  paragraph: string;
}

const BlogCta: React.FC<IBlogCta> = ({
  buttontxt,
  link,
  title,
  paragraph,
}): JSX.Element => (
  <div className={"btn-rompe-trafico"}>
    <Container pv={3}>
      <CtaBanner
        button1Link={link}
        button1Text={buttontxt}
        matomoAction={"Blog-internal-cta"}
        paragraph={paragraph}
        pv={4}
        size={"xs"}
        textSize={"medium"}
        title={title}
        variant={"dark"}
      />
    </Container>
  </div>
);

export { BlogCta };
