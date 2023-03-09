import React from "react";

import { Container } from "../../../../components/Container";
import { CtaBanner } from "../../../../components/CtaBanner";
import type { ICtaBannerProps } from "../../../../components/CtaBanner/types";

const SolutionCtaBanner: React.FC<ICtaBannerProps> = ({
  paragraph,
  title,
}): JSX.Element => (
  <Container bgColor={"#fff"} ph={4} pv={5}>
    <CtaBanner
      button1Link={"https://app.fluidattacks.com/SignUp"}
      button1Text={"Start free trial"}
      button2Link={"/contact-us/"}
      button2Text={"Contact now"}
      matomoAction={"Solution-free-trial"}
      paragraph={paragraph}
      size={"big"}
      sizeSm={"medium"}
      title={title}
    />
  </Container>
);

export { SolutionCtaBanner };
