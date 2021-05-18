declare module "gatsby-plugin-breadcrumb";
declare module "modal-video-custom";
declare module "*.png";
declare module "*.svg";

interface IQueryData {
  data: {
    asciidoc: {
      document: {
        title: string;
      };
      html: string;
      fields: {
        slug: string;
      };
      pageAttributes: {
        advise: string;
        alt: string;
        author: string;
        authors: string;
        banner: string;
        codename: string;
        cveid: string;
        date: string;
        defaux: string;
        definition: string;
        description: string;
        image: string;
        keywords: string;
        phrase: string;
        product: string;
        slug: string;
        solution: string;
        subtext: string;
        subtitle: string;
        writer: string;
      };
    };
  };
  pageContext: {
    breadcrumb: {
      location: string;
      crumbs: [
        {
          pathname: string;
          crumbLabel: string;
        }
      ];
    };
    slug: string;
  };
}
