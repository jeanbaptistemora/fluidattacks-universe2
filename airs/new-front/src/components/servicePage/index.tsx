/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation: 0 */
import { Link } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import {
  BannerContainer,
  BannerSubtitle,
  BannerTitle,
  FlexCenterItemsContainer,
  FullWidthContainer,
  PageArticle,
} from "../../styles/styledComponents";

interface IProps {
  banner: string;
  definition: string;
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

const ContentContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    mw-1366
    ph-body
    center
    roboto
  `,
})``;

const DefinitionContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    mw7
    center
    roboto
    f3-l
    f4
    fw3
    lh-2
    pv4
  `,
})``;

const ServicePage: React.FC<IProps> = ({
  banner,
  definition,
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

      <ContentContainer>
        <DefinitionContainer>{definition}</DefinitionContainer>
      </ContentContainer>
    </PageArticle>
  );
};

export { ServicePage };
