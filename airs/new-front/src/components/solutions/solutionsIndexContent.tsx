/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import {
  BlackListItemSpaced,
  FullWidthContainer,
  HalfScreenContainer,
  HalfScreenContainerSpaced,
  SolutionsParagraph,
  SolutionsSectionDescription,
  SolutionsSubtitle,
} from "../../styles/styledComponents";

interface IProps {
  image: string;
  imageAllignment: string;
  subtitle: string;
  paragraph: string;
  paragraphAllignment: string;
  padding?: string;
}

const SolutionsIndexContent: React.FC<IProps> = ({
  image,
  imageAllignment,
  subtitle,
  padding,
  paragraph,
  paragraphAllignment,
}: IProps): JSX.Element => (
  <FullWidthContainer className={"pv3 flex-l"}>
    <FullWidthContainer className={padding}>
      <HalfScreenContainer className={imageAllignment}>
        <img alt={"devSecOps Solution"} src={image} />
      </HalfScreenContainer>
      <HalfScreenContainerSpaced className={paragraphAllignment}>
        <SolutionsSectionDescription>
          <BlackListItemSpaced>
            <Link
              className={
                "c-fluid-bk underlined-animated no-underline mt0 mb3 t-all-5"
              }
              to={"."}>
              <SolutionsSubtitle>{subtitle}</SolutionsSubtitle>
            </Link>
            <SolutionsParagraph>{paragraph}</SolutionsParagraph>
          </BlackListItemSpaced>
        </SolutionsSectionDescription>
      </HalfScreenContainerSpaced>
    </FullWidthContainer>
  </FullWidthContainer>
);

// eslint-disable-next-line fp/no-mutation
SolutionsIndexContent.defaultProps = {
  padding: "",
};

export { SolutionsIndexContent };
