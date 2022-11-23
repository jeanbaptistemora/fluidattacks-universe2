/* eslint react/forbid-component-props: 0 */
import React from "react";

import {
  ArticleTitle,
  BannerContainer,
  BannerH2Title,
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
          {subtitle ? <BannerSubtitle>{subtitle}</BannerSubtitle> : undefined}
        </FullWidthContainer>
      </BannerContainer>
    );
  }

  return <ArticleTitle>{title}</ArticleTitle>;
};

export { PageHeader };
