/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";
import { BsArrowRightShort } from "react-icons/bs";

import { CardButton, CardContainer, Container } from "./styledComponents";

import { Paragraph, Title } from "../../Texts";

const PlansBanner: React.FC = (): JSX.Element => (
  <Container>
    <CardContainer>
      <Title fColor={"#2e2e38"} fSize={"36"}>
        {"Plans"}
      </Title>
      <Paragraph
        fColor={"#5c5c70"}
        fSize={"24"}
        marginBottom={"1"}
        marginTop={"1"}
      >
        {
          "Explore our plans in detail and get the power and control that you need to manage the security risks of your applications."
        }
      </Paragraph>
      <Link className={"no-underline"} to={"/plans"}>
        <CardButton>
          <Title fColor={"#2e2e38"} fSize={"24"}>
            {"Plans details"}
          </Title>
          <BsArrowRightShort />
        </CardButton>
      </Link>
    </CardContainer>
  </Container>
);

export { PlansBanner };
