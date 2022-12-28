import React from "react";

import { Container } from "../../../components/Container";
import { CtaBanner } from "../../../components/CtaBanner";
import { translate } from "../../../utils/translations/translate";

const CtaSection: React.FC = (): JSX.Element => (
  <Container bgColor={"#dddde3"} ph={4} pv={5}>
    <CtaBanner
      button1Link={"/free-trial/"}
      button1Text={"Start free trial"}
      button2Link={"/services/continuous-hacking/"}
      button2Text={"Learn more"}
      image={"/airs/blogs/blogs-cta"}
      matomoAction={"Blog-free-trial"}
      paragraph={translate.t("blog.ctaDescription")}
      size={"big"}
      sizeSm={"medium"}
      title={translate.t("blog.ctaTitle")}
    />
  </Container>
);

export { CtaSection };
