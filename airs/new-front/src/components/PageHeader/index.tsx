/* eslint react/forbid-component-props: 0 */
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import {
  ArticleTitle,
  BannerContainer,
  BannerSubtitle,
  BannerTitle,
  FullWidthContainer,
} from "../../styles/styledComponents";

interface IProps {
  banner: string;
  pageWithBanner: boolean;
  slug: string;
  subtext: string;
  subtitle: string;
  title: string;
}
const BannerH2Title: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    white
    fw7
    f1
    neue
    tc
    f-5-l
    ma0
  `,
})``;

const PageHeader: React.FC<IProps> = ({
  banner,
  pageWithBanner,
  slug,
  subtext,
  subtitle,
  title,
}: IProps): JSX.Element => {
  if (pageWithBanner) {
    if (slug === "careers/") {
      return (
        <BannerContainer className={banner}>
          <FullWidthContainer>
            <BannerH2Title>{subtitle}</BannerH2Title>
            <BannerSubtitle>{subtext}</BannerSubtitle>
          </FullWidthContainer>
        </BannerContainer>
      );
    }

    return (
      <BannerContainer className={banner}>
        <FullWidthContainer>
          <BannerTitle>{title}</BannerTitle>
        </FullWidthContainer>
      </BannerContainer>
    );
  }

  return <ArticleTitle>{title}</ArticleTitle>;
};

export { PageHeader };
