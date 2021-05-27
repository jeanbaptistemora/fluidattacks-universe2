/* eslint react/forbid-component-props:0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { AuthorsList } from "../../components/AuthorsList";
import { Layout } from "../../components/Layout";
import { NavbarComponent } from "../../components/Navbar";
import { Seo } from "../../components/Seo";
import { PageArticle } from "../../styles/styledComponents";
import { capitalizeCrumbs } from "../../utils/capitalizeCrumbs";

const authorsIndex: React.FC<IQueryData> = ({
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
        title={`Authors | Fluid Attacks`}
        url={"https://fluidattacks.com/blog/authors/"}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={"Authors"}
            crumbSeparator={" / "}
            crumbs={capitalizeCrumbs(crumbs)}
          />

          <PageArticle className={"internal"}>
            <AuthorsList />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default authorsIndex;
