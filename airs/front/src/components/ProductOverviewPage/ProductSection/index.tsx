import React, { useEffect, useState } from "react";

import { DemoBanner } from "./DemoBanner";
import {
  Container,
  ProgressBar,
  ProgressCol,
  ProgressContainer,
  SectionContainer,
} from "./styledComponents";

import { translate } from "../../../utils/translations/translate";

const ProductSection: React.FC = (): JSX.Element => {
  const data = [
    {
      description: translate.t(
        "productOverview.productSection.vulnDescription"
      ),
      hasHotSpot: true,
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
      hasHotSpot: true,
      image1: "remediation-1",
      image2: "remediation-2",
      imageRight: false,
      subtitle: translate.t(
        "productOverview.productSection.remediationSubtitle"
      ),
      title: translate.t("productOverview.productSection.remediationTitle"),
    },
    {
      description: translate.t(
        "productOverview.productSection.strictDescription"
      ),
      hasHotSpot: true,
      image1: "control-1",
      image2: "control-2",
      imageRight: true,
      subtitle: translate.t("productOverview.productSection.strictSubtitle"),
      title: translate.t("productOverview.productSection.strictTitle"),
    },
    {
      description: translate.t(
        "productOverview.productSection.analyticsDescription"
      ),
      hasHotSpot: true,
      image1: "analytics-1",
      image2: "analytics-2",
      imageRight: false,
      subtitle: translate.t("productOverview.productSection.analyticsSubtitle"),
      title: translate.t("productOverview.productSection.analyticsTitle"),
    },
    {
      description: translate.t(
        "productOverview.productSection.supportDescription"
      ),
      hasHotSpot: false,
      image1: "support",
      image2: "support",
      imageRight: true,
      subtitle: translate.t("productOverview.productSection.supportSubtitle"),
      title: translate.t("productOverview.productSection.supportTitle"),
    },
  ];

  const [scrollTop, setScrollTop] = useState(10);

  const onScroll = (): void => {
    const scrollDistance = -document
      .getElementsByClassName("product-section")[0]
      .getBoundingClientRect().top;
    const progressPercentage =
      (scrollDistance /
        (document
          .getElementsByClassName("product-section")[0]
          .getBoundingClientRect().height -
          document.documentElement.clientHeight)) *
      100;
    const scrolled = Math.floor(progressPercentage);

    if (scrolled <= 5) {
      setScrollTop(5);
    } else if (scrolled >= 100) {
      setScrollTop(100);
    } else {
      setScrollTop(scrolled);
    }
  };

  useEffect((): (() => void) => {
    window.addEventListener("scroll", onScroll);

    return (): void => {
      window.removeEventListener("scroll", onScroll);
    };
  }, []);

  return (
    <Container>
      <ProgressCol>
        <ProgressContainer>
          <ProgressBar height={`${scrollTop}`} />
        </ProgressContainer>
      </ProgressCol>
      <SectionContainer>
        {data.map((banner): JSX.Element => {
          return (
            <DemoBanner
              description={banner.description}
              hasHotSpot={banner.hasHotSpot}
              image1={banner.image1}
              image2={banner.image2}
              imageRight={banner.imageRight}
              key={banner.title}
              subtitle={banner.subtitle}
              title={banner.title}
            />
          );
        })}
      </SectionContainer>
    </Container>
  );
};

export { ProductSection };
