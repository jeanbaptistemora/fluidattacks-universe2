/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import { AnimationOnScroll } from "react-animation-on-scroll";

import {
  BlackListItemSpaced,
  FullWidthContainer,
  FullWidthContainerPlain,
  HalfScreenContainer,
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
      <AnimationOnScroll animateIn={animation} animateOnce={true}>
        <HalfScreenContainer>
          <Link to={link}>
            <img alt={"devSecOps Solution"} src={image} />
          </Link>
        </HalfScreenContainer>
      </AnimationOnScroll>
      <FullWidthContainerPlain>
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
                <button className={"button-white mt3"}>
                  {`Go to ${subtitle}`}
                </button>
              </Link>
            </SolutionsParagraph>
          </BlackListItemSpaced>
        </SolutionsSectionDescription>
      </FullWidthContainerPlain>
    </FullWidthContainer>
  </SolutionCardContainer>
);

export { SolutionsIndexContent };
