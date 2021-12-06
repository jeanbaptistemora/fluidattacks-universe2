declare module "gatsby-plugin-breadcrumb";
declare module "gatsby-plugin-transition-link/AniLink";
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
        image: string;
        keywords: string;
        partnersindex: string;
        phrase: string;
        product: string;
        slug: string;
        solution: string;
        subtext: string;
        subtitle: string;
        tags: string;
        title: string;
        writer: string;
      };
    };
    markdownRemark: {
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
        image: string;
        keywords: string;
        partnersindex: string;
        phrase: string;
        product: string;
        slug: string;
        solution: string;
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
  allAsciidoc: {
    edges: [
      {
        node: {
          fields: {
            slug: string;
          };
          document: {
            title: string;
          };
          html: string;
          pageAttributes: {
            advise: string;
            alt: string;
            author: string;
            authors: string;
            category: string;
            certification: string;
            certificationlogo: string;
            client: string;
            clientlogo: string;
            codename: string;
            cveid: string;
            date: string;
            filter: string;
            image: string;
            tags: string;
            description: string;
            partner: string;
            partnerlogo: string;
            product: string;
            slug: string;
            spanish: string;
            subtitle: string;
            writer: string;
          };
        };
      }
    ];
  };
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
            description: string;
            filter: string;
            image: string;
            partner: string;
            partnerlogo: string;
            product: string;
            slug: string;
            spanish: string;
            subtitle: string;
            tags: string;
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
      image: string;
      slug: string;
      spanish: string;
      subtitle: string;
      tags: string;
      title: string;
    };
  };
}
