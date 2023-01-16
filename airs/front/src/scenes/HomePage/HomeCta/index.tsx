import React from "react";

import { Container } from "../../../components/Container";
import { CtaBanner } from "../../../components/CtaBanner";
import { translate } from "../../../utils/translations/translate";

const HomeCta: React.FC = (): JSX.Element => {
  return (
    <Container bgColor={"#ffffff"} ph={4} pv={4}>
      <CtaBanner
        button1Link={"/free-trial/"}
        button1Text={"Start free trial"}
        button2Link={"/contact-us/"}
        button2Text={"Contact now"}
        image={"/airs/blogs/blogs-cta"}
        matomoAction={"Blogs-free-trial"}
        maxWidth={"1220px"}
        paragraph={translate.t("blog.ctaDescription")}
        pv={2}
        pvMd={4}
        pvSm={4}
        size={"small"}
        sizeSm={"small"}
        title={translate.t("blog.ctaTitle")}
      />
    </Container>
  );
};

export { HomeCta };
