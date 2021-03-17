import { InfoSection } from "./InfoSection";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import {
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
        <InfoSection />
      </InnerFooterInfoContainer>
    </MainFooterInfoContainer>
  </DarkBlueFooter>
);

export { Footer };
