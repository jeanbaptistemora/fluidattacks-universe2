declare module "gatsby-plugin-transition-link/AniLink";
declare module "*.png";
declare module "*.svg";

interface IQueryData {
  data: {
    markdownRemark: {
      htmlAst: string;
      html: string;
      fields: {
        slug: string;
      };
      frontmatter: {
        advise: string;
        alt: string;
        author: string;
        authors: string;
        banner: string;
        category: string;
        certificationid: string;
        certificationsindex: string;
        clientsindex: string;
        codename: string;
        cveid: string;
        date: string;
        defaux: string;
        definition: string;
        description: string;
        encrypted: string;
        headtitle: string;
        identifier: string;
        image: string;
        keywords: string;
        modified: string;
        partnersindex: string;
        phrase: string;
        product: string;
        slug: string;
        subtext: string;
        subtitle: string;
        product: string;
        tags: string;
        template: string;
        title: string;
        writer: string;
      };
      rawMarkdownBody: string;
    };
    site: {
      siteMetadata: {
        author: string;
        description: string;
        keywords: string;
        siteUrl: string;
        title: string;
      };
    };
  };
  pageContext: {
    authorName: string;
    breadcrumb: {
      location: string;
      crumbs: [
        {
          pathname: string;
          crumbLabel: string;
        }
      ];
    };
    categoryName: string;
    tagName: string;
    slug: string;
  };
}

interface IData {
  allMarkdownRemark: {
    edges: [
      {
        node: {
          fields: {
            slug: string;
          };
          html: string;
          frontmatter: {
            advise: string;
            alt: string;
            author: string;
            authors: string;
            category: string;
            certification: string;
            certificationidd: string;
            certificationlogo: string;
            client: string;
            clientlogo: string;
            codename: string;
            cveid: string;
            date: string;
            definition: string;
            description: string;
            encrypted: string;
            filter: string;
            identifier: string;
            image: string;
            partner: string;
            partnerlogo: string;
            product: string;
            severity: string;
            slug: string;
            spanish: string;
            subtitle: string;
            tags: string;
            template: string;
            title: string;
            writer: string;
          };
        };
      }
    ];
  };
}

interface INodes {
  node: {
    fields: {
      slug: string;
    };
    frontmatter: {
      alt: string;
      author: string;
      category: string;
      certification: string;
      date: string;
      description: string;
      identifier: string;
      image: string;
      slug: string;
      spanish: string;
      subtitle: string;
      tags: string;
      title: string;
    };
  };
}
