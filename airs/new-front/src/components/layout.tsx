import React from "react";
import {
  CopyrightContainer,
  CopyrightParagraph,
  FooterInfoLink,
  FooterInfoLinksContainer,
  GrayDash,
  InnerFooterInfoContainer,
  MainFooterInfoContainer,
} from "../styles/styledComponents";
import { graphql, useStaticQuery } from "gatsby";

import "tachyons/css/tachyons.min.css";
import "../styles/index.scss";

interface IChildrenProps {
  children: JSX.Element;
}

interface ISiteMetadata {
  site: {
    siteMetadata: {
      url: string;
    };
  };
}

const Layout: React.FC<IChildrenProps> = ({
  children,
}: IChildrenProps): JSX.Element => {
  const { site }: ISiteMetadata = useStaticQuery(
    // eslint-disable-next-line @typescript-eslint/no-confusing-void-expression
    graphql`
      query {
        site {
          siteMetadata {
            url
          }
        }
      }
    `
  );

  return (
    <React.StrictMode>
      <div>
        <main>{children}</main>
        <footer>
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
                <FooterInfoLink href={`${site.siteMetadata.url}/terms-use/`}>
                  {"Terms of Use"}
                </FooterInfoLink>
                <GrayDash>{" - "}</GrayDash>
                <FooterInfoLink href={`${site.siteMetadata.url}/privacy/`}>
                  {"Privacy Policy"}
                </FooterInfoLink>
                <GrayDash>{" - "}</GrayDash>
                <FooterInfoLink href={`${site.siteMetadata.url}/cookie/`}>
                  {"Cookie Policy"}
                </FooterInfoLink>
              </FooterInfoLinksContainer>
            </InnerFooterInfoContainer>
          </MainFooterInfoContainer>
        </footer>
      </div>
    </React.StrictMode>
  );
};

export { Layout };
