import React from "react";

import { Container } from "../../../components/Container";
import { CtaBanner } from "../../../components/CtaBanner";

const SubscribeSection: React.FC = (): JSX.Element => {
  return (
    <Container ph={4} pv={5}>
      <Container center={true} maxWidth={"1000px"}>
        <CtaBanner
          button1Link={"/subscription/"}
          button1Text={"Subscribe"}
          matomoAction={"blog-internal-subscribe"}
          paragraph={"Sign up for Fluid Attacks’ weekly newsletter."}
          sizeMd={"medium"}
          title={"Subscribe to our blog"}
        />
      </Container>
    </Container>
  );
};

export { SubscribeSection };
