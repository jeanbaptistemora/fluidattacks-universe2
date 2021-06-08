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
import { capitalizeCrumbs } from "../utils/capitalizeCrumbs";
import { translate } from "../utils/translations/translate";

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

  const { title } = data.asciidoc.document;
  const customCrumbLabel: string = `${title
    .charAt(0)
    .toUpperCase()}${title.slice(1).replace("-", "")}`;

  let isContinuous: string = "";
  let image: string = "";

  if (data.asciidoc.pageAttributes.slug === "services/continuous-hacking/") {
    isContinuous = "yes";
    image = continuousImage;
  } else {
    isContinuous = "no";
    image = oneShotImage;
  }

  return (
    <React.Fragment>
      <Seo
        description={data.asciidoc.pageAttributes.description}
        image={data.asciidoc.pageAttributes.image.replace(".webp", ".png")}
        keywords={data.asciidoc.pageAttributes.keywords}
        title={`${title} | Fluid Attacks`}
        url={data.asciidoc.pageAttributes.slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={customCrumbLabel}
            crumbSeparator={" / "}
            crumbs={capitalizeCrumbs(crumbs)}
          />

          <ServicePage
            banner={data.asciidoc.pageAttributes.banner}
            content={data.asciidoc.html}
            definition={data.asciidoc.pageAttributes.definition}
            image={image}
            isContinuous={isContinuous}
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
    asciidoc(fields: { slug: { eq: $slug } }) {
      document {
        title
      }
      html
      fields {
        slug
      }
      pageAttributes {
        banner
        image
        definition
        description
        keywords
        slug
      }
    }
  }
`;
