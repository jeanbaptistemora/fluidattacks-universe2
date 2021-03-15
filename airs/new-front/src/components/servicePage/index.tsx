/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation: 0 */
import { Link } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import {
  ArticleContainer,
  BannerContainer,
  BannerSubtitle,
  BannerTitle,
  FlexCenterItemsContainer,
  FullWidthContainer,
  PageArticle,
  PageContainer,
} from "../../styles/styledComponents";

interface IProps {
  banner: string;
  isContinuous: string;
  subtitle: string;
  title: string;
}

interface IItemsProps {
  continuous: string;
  oneShot: string;
}

const SubmenuListItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
    dib
    ph2
  `,
})``;

const ServicePage: React.FC<IProps> = ({
  banner,
  isContinuous,
  subtitle,
  title,
}: IProps): JSX.Element => {
  const subMenuClasses: IItemsProps = {
    continuous: "",
    oneShot: "",
  };

  const linksClasses: IItemsProps = {
    continuous: "c-fluid-bk",
    oneShot: "c-fluid-bk",
  };
  if (isContinuous === "yes") {
    subMenuClasses.continuous = "bb bc-hovered-red bw2";
    linksClasses.oneShot = "c-fluid-gray hv-fluid-black";
  } else {
    subMenuClasses.oneShot = "bb bc-hovered-red bw2";
    linksClasses.continuous = "c-fluid-gray hv-fluid-black";
  }

  return (
    <PageArticle>
      <BannerContainer className={banner}>
        <FullWidthContainer>
          <BannerTitle>{title}</BannerTitle>
          <BannerSubtitle>{subtitle}</BannerSubtitle>
        </FullWidthContainer>
      </BannerContainer>
      <ArticleContainer>
        <FlexCenterItemsContainer className={"tc pt3 nowrap overflow-x-auto"}>
          <ul className={"pl0"}>
            <SubmenuListItem className={subMenuClasses.continuous}>
              <Link
                className={`${linksClasses.continuous} f4 roboto fw7 no-underline`}
                to={"/services/continuous-hacking/"}>
                {"Continuous Hacking"}
              </Link>
            </SubmenuListItem>
            <SubmenuListItem className={subMenuClasses.oneShot}>
              <Link
                className={`${linksClasses.oneShot} f4 roboto fw7 no-underline`}
                to={"/services/one-shot-hacking/"}>
                {"One-Shot Hacking"}
              </Link>
            </SubmenuListItem>
          </ul>
        </FlexCenterItemsContainer>
        <PageContainer />
      </ArticleContainer>
    </PageArticle>
  );
};

export { ServicePage };
