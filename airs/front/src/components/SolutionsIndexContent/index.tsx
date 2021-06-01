/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import ScrollAnimation from "react-animate-on-scroll";

import {
  BlackListItemSpaced,
  FullWidthContainer,
  HalfScreenContainer,
  HalfScreenContainerSpaced,
  SolutionCardContainer,
  SolutionsParagraph,
  SolutionsSectionDescription,
  SolutionsSubtitle,
} from "../../styles/styledComponents";

interface IProps {
  animation: string;
  image: string;
  link: string;
  subtitle: string;
  paragraph: string;
}

const SolutionsIndexContent: React.FC<IProps> = ({
  animation,
  image,
  link,
  subtitle,
  paragraph,
}: IProps): JSX.Element => (
  <SolutionCardContainer>
    <FullWidthContainer>
      <ScrollAnimation animateIn={animation} animateOnce={true}>
        <HalfScreenContainer>
          <img alt={"devSecOps Solution"} src={image} />
        </HalfScreenContainer>
      </ScrollAnimation>
      <HalfScreenContainerSpaced>
        <SolutionsSectionDescription>
          <BlackListItemSpaced>
            <SolutionsSubtitle>{subtitle}</SolutionsSubtitle>
            <SolutionsParagraph>{paragraph}</SolutionsParagraph>
            <SolutionsParagraph>
              <Link
                className={
                  "c-fluid-bk f5 mt6 hv-fluid-rd fw4 no-underline t-all-5"
                }
                to={link}
              >
                {`Go to ${subtitle} >`}
              </Link>
            </SolutionsParagraph>
          </BlackListItemSpaced>
        </SolutionsSectionDescription>
      </HalfScreenContainerSpaced>
    </FullWidthContainer>
  </SolutionCardContainer>
);

export { SolutionsIndexContent };
