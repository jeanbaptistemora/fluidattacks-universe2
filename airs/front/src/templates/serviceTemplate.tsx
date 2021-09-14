/*
 *There is no danger using dangerouslySetInnerHTML since everything is built in
 *compile time, also
 *Default exports are needed for pages used in nodes by default to create pages
 *like index.tsx or this one
 */
/* eslint import/no-default-export:0 */
/* eslint fp/no-let: 0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint fp/no-mutation: 0 */
/* eslint import/no-namespace:0 */
import { graphql } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { ServicePage } from "../components/ServicePage";
import { translate } from "../utils/translations/translate";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const continuousImage: string =
  "https://res.cloudinary.com/fluid-attacks/image/upload/v1619722210/airs/services/service-continuous_qyvqv8.webp";
const oneShotImage: string =
  "https://res.cloudinary.com/fluid-attacks/image/upload/v1619722210/airs/services/service-one-shot_pjqgnf.webp";

const ContinuousHackingIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const {
    banner,
    definition,
    description,
    image,
    keywords,
    slug,
    title,
  } = data.markdownRemark.frontmatter;

  const currentService =
    slug === "services/continuous-hacking/"
      ? { isContinuous: "yes", serviceImage: continuousImage }
      : { isContinuous: "no", serviceImage: oneShotImage };

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={image.replace(".webp", ".png")}
        keywords={keywords}
        title={`${title} | Fluid Attacks`}
        url={slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={capitalizePlainString(title)}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <ServicePage
            banner={banner}
            content={data.markdownRemark.html}
            definition={definition}
            image={currentService.serviceImage}
            isContinuous={currentService.isContinuous}
            subtitle={translate.t("service.subTitle")}
            title={title}
          />
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default ContinuousHackingIndex;

export const query: void = graphql`
  query ContinuousHackingIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        banner
        image
        definition
        description
        keywords
        slug
        title
      }
    }
  }
`;
