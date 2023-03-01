/* eslint react/forbid-component-props: 0 */
import React from "react";

import { BlogSeo } from "../components/BlogSeo";
import { Breadcrumbs } from "../components/Breadcrumbs";
import { Seo } from "../components/Seo";
import { BlogsToFilterPage } from "../scenes/BlogsToFilterPage";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import { PageArticle } from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";
import { capitalizeDashedString, stringToUri } from "../utils/utilities";

const blogAuthorTemplate: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const { location } = pageContext.breadcrumb;

  const home = ["/"];
  const path = home.concat(
    location.split("/").filter((name): boolean => name !== "")
  );

  const { authorName } = pageContext;
  const blogImage: string =
    "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632208/airs/bg-blog_bj0szx.png";

  const data = [
    {
      description: translate.t("blogListAuthors.alejandroHerrera.description"),
      metaDescription: translate.t(
        "blogListAuthors.alejandroHerrera.metaDescription"
      ),
      title: translate.t("blogListAuthors.alejandroHerrera.title"),
    },
    {
      description: translate.t("blogListAuthors.andersonTaguada.description"),
      metaDescription: translate.t(
        "blogListAuthors.andersonTaguada.metaDescription"
      ),
      title: translate.t("blogListAuthors.andersonTaguada.title"),
    },
    {
      description: translate.t("blogListAuthors.andresCuberos.description"),
      metaDescription: translate.t(
        "blogListAuthors.andresCuberos.metaDescription"
      ),
      title: translate.t("blogListAuthors.andresCuberos.title"),
    },
    {
      description: translate.t("blogListAuthors.andresRoldan.description"),
      metaDescription: translate.t(
        "blogListAuthors.andresRoldan.metaDescription"
      ),
      title: translate.t("blogListAuthors.andresRoldan.title"),
    },
    {
      description: translate.t("blogListAuthors.andresTirado.description"),
      metaDescription: translate.t(
        "blogListAuthors.andresTirado.metaDescription"
      ),
      title: translate.t("blogListAuthors.andresTirado.title"),
    },
    {
      description: translate.t("blogListAuthors.carlosBello.description"),
      metaDescription: translate.t(
        "blogListAuthors.carlosBello.metaDescription"
      ),
      title: translate.t("blogListAuthors.carlosBello.title"),
    },
    {
      description: translate.t("blogListAuthors.danielSalazar.description"),
      metaDescription: translate.t(
        "blogListAuthors.danielSalazar.metaDescription"
      ),
      title: translate.t("blogListAuthors.danielSalazar.title"),
    },
    {
      description: translate.t("blogListAuthors.danielYepes.description"),
      metaDescription: translate.t(
        "blogListAuthors.danielYepes.metaDescription"
      ),
      title: translate.t("blogListAuthors.danielYepes.title"),
    },
    {
      description: translate.t("blogListAuthors.diegoAlvarez.description"),
      metaDescription: translate.t(
        "blogListAuthors.diegoAlvarez.metaDescription"
      ),
      title: translate.t("blogListAuthors.diegoAlvarez.title"),
    },
    {
      description: translate.t("blogListAuthors.felipeGomez.description"),
      metaDescription: translate.t(
        "blogListAuthors.felipeGomez.metaDescription"
      ),
      title: translate.t("blogListAuthors.felipeGomez.title"),
    },
    {
      description: translate.t("blogListAuthors.felipeRuiz.description"),
      metaDescription: translate.t(
        "blogListAuthors.felipeRuiz.metaDescription"
      ),
      title: translate.t("blogListAuthors.felipeRuiz.title"),
    },
    {
      description: translate.t("blogListAuthors.felipeZarate.description"),
      metaDescription: translate.t(
        "blogListAuthors.felipeZarate.metaDescription"
      ),
      title: translate.t("blogListAuthors.felipeZarate.title"),
    },
    {
      description: translate.t("blogListAuthors.jasonChavarria.description"),
      metaDescription: translate.t(
        "blogListAuthors.jasonChavarria.metaDescription"
      ),
      title: translate.t("blogListAuthors.jasonChavarria.title"),
    },
    {
      description: translate.t("blogListAuthors.jonathanArmas.description"),
      metaDescription: translate.t(
        "blogListAuthors.jonathanArmas.metaDescription"
      ),
      title: translate.t("blogListAuthors.jonathanArmas.title"),
    },
    {
      description: translate.t("blogListAuthors.juanAguirre.description"),
      metaDescription: translate.t(
        "blogListAuthors.juanAguirre.metaDescription"
      ),
      title: translate.t("blogListAuthors.juanAguirre.title"),
    },
    {
      description: translate.t("blogListAuthors.julianArango.description"),
      metaDescription: translate.t(
        "blogListAuthors.julianArango.metaDescription"
      ),
      title: translate.t("blogListAuthors.julianArango.title"),
    },
    {
      description: translate.t("blogListAuthors.kevinAmado.description"),
      metaDescription: translate.t(
        "blogListAuthors.kevinAmado.metaDescription"
      ),
      title: translate.t("blogListAuthors.kevinAmado.title"),
    },
    {
      description: translate.t("blogListAuthors.kevinCardona.description"),
      metaDescription: translate.t(
        "blogListAuthors.kevinCardona.metaDescription"
      ),
      title: translate.t("blogListAuthors.kevinCardona.title"),
    },
    {
      description: translate.t("blogListAuthors.mateoGutierrez.description"),
      metaDescription: translate.t(
        "blogListAuthors.mateoGutierrez.metaDescription"
      ),
      title: translate.t("blogListAuthors.mateoGutierrez.title"),
    },
    {
      description: translate.t("blogListAuthors.mauricioGomez.description"),
      metaDescription: translate.t(
        "blogListAuthors.mauricioGomez.metaDescription"
      ),
      title: translate.t("blogListAuthors.mauricioGomez.title"),
    },
    {
      description: translate.t("blogListAuthors.oscarPrado.description"),
      metaDescription: translate.t(
        "blogListAuthors.oscarPrado.metaDescription"
      ),
      title: translate.t("blogListAuthors.oscarPrado.title"),
    },
    {
      description: translate.t("blogListAuthors.oscarUribe.description"),
      metaDescription: translate.t(
        "blogListAuthors.oscarUribe.metaDescription"
      ),
      title: translate.t("blogListAuthors.oscarUribe.title"),
    },
    {
      description: translate.t("blogListAuthors.oswaldoParada.description"),
      metaDescription: translate.t(
        "blogListAuthors.oswaldoParada.metaDescription"
      ),
      title: translate.t("blogListAuthors.oswaldoParada.title"),
    },
    {
      description: translate.t("blogListAuthors.rafaelBallestas.description"),
      metaDescription: translate.t(
        "blogListAuthors.rafaelBallestas.metaDescription"
      ),
      title: translate.t("blogListAuthors.rafaelBallestas.title"),
    },
    {
      description: translate.t("blogListAuthors.rafaelAlvarez.description"),
      metaDescription: translate.t(
        "blogListAuthors.rafaelAlvarez.metaDescription"
      ),
      title: translate.t("blogListAuthors.rafaelAlvarez.title"),
    },
    {
      description: translate.t(
        "blogListAuthors.sebastianVillalobos.description"
      ),
      metaDescription: translate.t(
        "blogListAuthors.sebastianVillalobos.metaDescription"
      ),
      title: translate.t("blogListAuthors.sebastianVillalobos.title"),
    },
  ];

  const authorTitle = data.find(
    (tag): boolean => stringToUri(tag.title) === authorName
  )?.title;

  const authorDescription = data.find(
    (tag): boolean => stringToUri(tag.title) === authorName
  )?.description;

  const metaDescription = data.find(
    (tag): boolean => stringToUri(tag.title) === authorName
  )?.metaDescription;

  return (
    <React.Fragment>
      <Seo
        description={
          metaDescription === undefined
            ? translate.t("blog.description")
            : metaDescription
        }
        image={blogImage}
        keywords={translate.t("blog.keywords")}
        title={`Blog posts by ${capitalizeDashedString(
          authorName
        )} | Application security testing solutions | Fluid Attacks`}
        url={`https://fluidattacks.com/blog/authors/${authorName}`}
      />
      <BlogSeo
        description={
          metaDescription === undefined
            ? translate.t("blog.description")
            : metaDescription
        }
        image={blogImage}
        title={"Blog | Application security testing solutions | Fluid Attacks"}
        url={"https://fluidattacks.com/blog"}
      />

      <Layout>
        <div>
          <NavbarComponent />

          <Breadcrumbs currentPath={path} />
          <PageArticle bgColor={"transparent"}>
            <BlogsToFilterPage
              description={authorDescription}
              filterBy={"author"}
              title={
                authorTitle === undefined
                  ? undefined
                  : `Posts by ${authorTitle}`
              }
              value={authorName}
            />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default blogAuthorTemplate;
