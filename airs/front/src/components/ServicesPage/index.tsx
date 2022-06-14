/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
import { Link, graphql, useStaticQuery } from "gatsby";
import React from "react";

import { CardContainer, Container } from "./styledComponents";

import { PhantomRegularRedButton } from "../../styles/styledComponents";
import { CloudImage } from "../CloudImage";
import { Paragraph, Title } from "../Texts";

const ServicesPage: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query ServicesQuery {
      allMarkdownRemark(sort: { fields: [frontmatter___slug], order: ASC }) {
        edges {
          node {
            fields {
              slug
            }
            frontmatter {
              definition
              slug
              title
              image
              template
            }
          }
        }
      }
    }
  `);

  const servicesCards = data.allMarkdownRemark.edges.filter(
    (serviceCard): boolean =>
      serviceCard.node.frontmatter.template === "service"
  );

  return (
    <Container>
      {servicesCards.map((serviceCard): JSX.Element => {
        const { definition, image, slug, title } = serviceCard.node.frontmatter;

        return (
          <CardContainer key={title}>
            <CloudImage alt={title} src={`airs/${image}`} styles={"w-100"} />
            <Title
              fColor={"#2e2e38"}
              fSize={"24"}
              marginBottom={"1"}
              marginTop={"1"}
            >
              {title}
            </Title>
            <Paragraph fColor={"#5c5c70"} fSize={"16"} marginBottom={"1"}>
              {definition}
            </Paragraph>
            <Link to={`/${slug}`}>
              <PhantomRegularRedButton>
                {"Go to service"}
              </PhantomRegularRedButton>
            </Link>
          </CardContainer>
        );
      })}
    </Container>
  );
};

export { ServicesPage };
