/* eslint react/forbid-component-props:0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { Layout } from "../../components/Layout";
import { NavbarComponent } from "../../components/Navbar";
import { Seo } from "../../components/Seo";
import { TagsList } from "../../components/TagsList";
import { PageArticle } from "../../styles/styledComponents";
import { capitalizeObject } from "../../utils/utilities";

const tagsIndex: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  return (
    <React.Fragment>
      <Seo
        description={""}
        keywords={""}
        title={`Tags | Fluid Attacks`}
        url={"https://fluidattacks.com/blog/tags/"}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={"Tags"}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle className={"internal"}>
            <TagsList />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default tagsIndex;
