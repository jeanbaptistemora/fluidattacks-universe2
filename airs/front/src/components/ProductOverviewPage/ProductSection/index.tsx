/* eslint react/forbid-component-props: 0 */
import React, { useEffect, useState } from "react";

import { DemoBanner } from "./DemoBanner";
import {
  Container,
  HorizontalProgressBar,
  HorizontalProgressContainer,
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

  const [scrollTop, setScrollTop] = useState(5);
  const [scrollHorizontal, setScrollHorizontal] = useState(5);

  const onScroll = (): void => {
    const scrollDistance = -document
      .getElementsByClassName("product-section")[0]
      .getBoundingClientRect().top;
    const progressPercentage =
      document.getElementsByClassName("product-section")[0].scrollHeight -
      document.documentElement.clientHeight;
    const scrolled = (scrollDistance / progressPercentage) * 100;

    if (scrolled <= 5) {
      setScrollTop(5);
    } else if (scrolled >= 100) {
      setScrollTop(100);
    } else {
      setScrollTop(scrolled);
    }
  };

  const onHorizontalScroll = (): void => {
    const scrollDistance =
      document.getElementsByClassName("product-section")[0].scrollLeft;
    const progressPercentage =
      document.getElementsByClassName("product-section")[0].scrollWidth -
      document.getElementsByClassName("product-section")[0].clientWidth;
    const scrolled = (scrollDistance / progressPercentage) * 100;

    if (scrolled <= 5) {
      setScrollHorizontal(5);
    } else if (scrolled >= 100) {
      setScrollHorizontal(100);
    } else {
      setScrollHorizontal(scrolled);
    }
  };

  useEffect((): (() => void) => {
    const productSection = document.getElementsByClassName("product-section");

    window.addEventListener("scroll", onScroll);
    productSection[0].addEventListener("scroll", onHorizontalScroll);

    return (): void => {
      window.removeEventListener("scroll", onScroll);
      productSection[0].removeEventListener("scroll", onHorizontalScroll);
    };
  }, []);

  return (
    <Container>
      <ProgressCol>
        <ProgressContainer>
          <ProgressBar style={{ height: `${scrollTop}%` }} />
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
      <HorizontalProgressContainer>
        <HorizontalProgressBar style={{ width: `${scrollHorizontal}%` }} />
      </HorizontalProgressContainer>
    </Container>
  );
};

export { ProductSection };
