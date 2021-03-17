/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import {
  CopyrightContainer,
  CopyrightParagraph,
  FooterInfoLink,
  FooterInfoLinksContainer,
  GrayDash,
  InnerFooterInfoContainer,
  MainFooterInfoContainer,
} from "../../styles/styledComponents";

const DarkBlueFooter: StyledComponent<
  "footer",
  Record<string, unknown>
> = styled.footer.attrs({
  className: `
    bg-darker-blue
  `,
})``;

const Footer: React.FC = (): JSX.Element => (
  <DarkBlueFooter>
    <MainFooterInfoContainer>
      <InnerFooterInfoContainer>
        <CopyrightContainer>
          <CopyrightParagraph>
            {`Copyright © ${new Date().getFullYear()} Fluid Attacks, We hack
              your software. All rights reserved.`}
          </CopyrightParagraph>
        </CopyrightContainer>
        <FooterInfoLinksContainer>
          <FooterInfoLink href={"https://status.fluidattacks.com/"}>
            {"Service status"}
          </FooterInfoLink>
          <GrayDash>{" - "}</GrayDash>
          <Link
            className={
              "c-blue-gray f6 fw2 mt2 roboto no-underline hv-fluid-dkred"
            }
            to={"/terms-use/"}>
            {"Terms of Use"}
          </Link>
          <GrayDash>{" - "}</GrayDash>
          <Link
            className={
              "c-blue-gray f6 fw2 mt2 roboto no-underline hv-fluid-dkred"
            }
            to={"/privacy/"}>
            {"Privacy Policy"}
          </Link>
          <GrayDash>{" - "}</GrayDash>
          <Link
            className={
              "c-blue-gray f6 fw2 mt2 roboto no-underline hv-fluid-dkred"
            }
            to={"/cookie"}>
            {"Cookie Policy"}
          </Link>
        </FooterInfoLinksContainer>
      </InnerFooterInfoContainer>
    </MainFooterInfoContainer>
  </DarkBlueFooter>
);

export { Footer };
