import React from "react";

import { DemoBanner } from "./DemoBanner";
import { Container } from "./styledComponents";

import { translate } from "../../../utils/translations/translate";

const ProductSection: React.FC = (): JSX.Element => {
  const data = [
    {
      description: translate.t(
        "productOverview.productSection.vulnDescription"
      ),
      image1: "vulnerabilities-1",
      image2: "vulnerabilities-2",
      imageRight: true,
      subtitle: translate.t("productOverview.productSection.vulnSubtitle"),
      title: translate.t("productOverview.productSection.vulnTitle"),
    },
    {
      description: translate.t(
        "productOverview.productSection.remediationDescription"
      ),
      image1: "remediation-1",
      image2: "remediation-2",
      imageRight: false,
      subtitle: translate.t(
        "productOverview.productSection.remediationSubtitle"
      ),
      title: translate.t("productOverview.productSection.remediationTitle"),
    },
  ];

  return (
    <Container>
      {data.map((banner): JSX.Element => {
        return (
          <DemoBanner
            description={banner.description}
            image1={banner.image1}
            image2={banner.image2}
            imageRight={banner.imageRight}
            key={banner.title}
            subtitle={banner.subtitle}
            title={banner.title}
          />
        );
      })}
    </Container>
  );
};

export { ProductSection };
