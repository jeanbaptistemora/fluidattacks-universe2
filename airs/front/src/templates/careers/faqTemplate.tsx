/* eslint react/no-danger:0 */
/* eslint import/no-default-export:0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation: 0 */
import { graphql } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import { decode } from "he";
import React, { useEffect } from "react";

import { Layout } from "../../components/Layout";
import { NavbarComponent } from "../../components/Navbar";
import { PageHeader } from "../../components/PageHeader";
import { Seo } from "../../components/Seo";
import { FaqContainer, PageArticle } from "../../styles/styledComponents";
import { capitalizeObject, capitalizePlainString } from "../../utils/utilities";

const FaqIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { title } = data.asciidoc.document;
  const {
    banner,
    description,
    keywords,
    slug,
    subtext,
    subtitle,
  } = data.asciidoc.pageAttributes;

  const hasBanner: boolean = typeof banner === "string";

  const setArrows = (): void => {
    document.querySelectorAll("h4").forEach((question): void => {
      question.classList.add("arrow-down");
    });
  };

  const setOnclick = (): void => {
    document.querySelectorAll(".sect3").forEach((element): void => {
      (element as HTMLElement).onclick = (): void => {
        element.querySelectorAll(".paragraph").forEach((paragraph): void => {
          const isShow = Array.from(paragraph.classList).includes("db");
          if (isShow) {
            paragraph.classList.remove("db");
          } else {
            paragraph.classList.add("db");
          }
        });
        element.querySelectorAll(".olist").forEach((paragraph): void => {
          const isShow = Array.from(paragraph.classList).includes("db");
          if (isShow) {
            paragraph.classList.remove("db");
          } else {
            paragraph.classList.add("db");
          }
        });
        element.querySelectorAll("h4").forEach((question): void => {
          const isShow = Array.from(question.classList).includes("arrow-up");
          if (isShow) {
            question.classList.remove("arrow-up");
            question.classList.add("arrow-down");
          } else {
            question.classList.remove("arrow-down");
            question.classList.add("arrow-up");
          }
        });
      };
    });
  };

  useEffect((): void => {
    setArrows();
    setOnclick();
  }, []);

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/c_scale,w_1200/v1622583388/airs/logo_fluid_attacks_2021_eqop3k.png"
        }
        keywords={keywords}
        title={decode(`${title} | Fluid Attacks`)}
        url={slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={decode(capitalizePlainString(title))}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle>
            <PageHeader
              banner={banner}
              pageWithBanner={hasBanner}
              slug={slug}
              subtext={subtext}
              subtitle={subtitle}
              title={decode(title)}
            />
            <FaqContainer
              className={"internal faq-page"}
              dangerouslySetInnerHTML={{
                __html: data.asciidoc.html,
              }}
            />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default FaqIndex;

export const query: void = graphql`
  query CareersFaqIndex($slug: String!) {
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
        description
        keywords
        slug
        subtext
        subtitle
      }
    }
  }
`;
