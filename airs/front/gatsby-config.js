module.exports = {
  flags: {
    DEV_SSR: true,
  },
  pathPrefix: '/front',
  trailingSlash: 'always',
  siteMetadata: {
    author: "Fluid Attacks",
    description:
      'Our application security testing combines automation and penetration testing '
      + 'to find all vulnerabilities so you can deploy secure software, achieve '
      + 'DevSecOps and reduce cyber risks.',
    keywords:
      "Fluid Attacks, Pentesting, Ethical Hacking, Security Testing, Cybersecurity",
    siteUrl: "https://fluidattacks.com", // No trailing slash allowed!
    title: "Application security testing solutions | Fluid Attacks",
  },
  plugins: [
    "gatsby-plugin-sass",
    {
      resolve: "gatsby-plugin-web-font-loader",
      options: {
        google: {
          families: ["Poppins:400,700"],
        },
      },
    },
    {
      resolve: "gatsby-source-cloudinary",
      options: {
        apiKey: process.env.CLOUDINARY_API_KEY,
        apiSecret: process.env.CLOUDINARY_API_SECRET,
        cloudName: process.env.CLOUDINARY_CLOUD_NAME,
        maxResults: 1000,
        prefix: "airs/",
        resourceType: "image",
      },
    },
    {
      resolve: `gatsby-plugin-feed`,
      options: {
        query: `
          {
            site {
              siteMetadata {
                title
                description
                siteUrl
                site_url: siteUrl
              }
            }
          }
        `,
        feeds: [
          {
            serialize: ({ query: { site, allMarkdownRemark } }) => {
              return allMarkdownRemark.nodes.map(node => {
                return Object.assign({}, node.frontmatter, {
                  date: node.frontmatter.date,
                  url: site.siteMetadata.siteUrl + node.fields.slug,
                  guid: site.siteMetadata.siteUrl + node.fields.slug,
                  custom_elements: [{ "content:encoded": node.html }],
                })
              })
            },
            query: `
              {
                allMarkdownRemark(
                  filter: {
                    fields: { slug: { regex: "/blog/" } }
                  },
                  sort: { order: DESC, fields: [frontmatter___date] },
                ) {
                  nodes {
                    html
                    fields {
                      slug
                    }
                    frontmatter {
                      title
                      description
                      date
                      author
                    }
                  }
                }
              }
            `,

            output: "/rss.xml",
            title: "Fluid Attacks RSS Feed",
          },
        ],
      },
    },
    {
      resolve: "gatsby-source-filesystem",
      options: {
        path: "content",
        name: "pages",
      },
    },
    {
      resolve: `gatsby-transformer-remark`,
      options: {
        plugins: [
          {
            resolve: "gatsby-remark-component-parent2div",
            options: {
              components: ["time-lapse"]
            }
          },
          {
            resolve: `gatsby-remark-classes`,
            options: {
              classMap: {
                link: "basic-link"
              }
            }
          }
        ],
      },
    },
    {
      resolve: "gatsby-plugin-google-tagmanager",
      options: {
        id: "GTM-PCDDL8T",

        // Include GTM in development.
        //
        // Defaults to false meaning GTM will only be loaded in production.
        includeInDevelopment: false,

        // datalayer to be set before GTM is loaded
        // should be an object or a function that is executed in the browser
        //
        // Defaults to null
        defaultDataLayer: { platform: "gatsby" },
      },
    },
    {
      resolve: "gatsby-plugin-web-font-loader",
      options: {
        typekit: {
          id: "gtl3fqb",
        },
      },
    },
    {
      resolve: "gatsby-plugin-algolia",
      options: {
        appId: process.env.GATSBY_ALGOLIA_APP_ID,
        apiKey: process.env.ALGOLIA_ADMIN_KEY,
        enablePartialUpdates: true,
        /* (optional) Fields to use for comparing if the index object is different from the new one */
        /* By default it uses a field called "modified" which could be a boolean | datetime string */
        matchFields: ["slug", "modified"], // Array<String> default: ['modified']
        queries: require("./src/utils/algolia-queries"),
      },
    },
    {
      resolve: "gatsby-plugin-sitemap",
      options: {
        excludes: [`/blog/authors/**`, `/blog/tags/**`, `/blog/categories/**`],
      },
    },
    {
      resolve: "gatsby-plugin-robots-txt",
      options: {
        policy: [
          {
            userAgent: "*",
            allow: ["/", "/css/*.css", "/css/*.css$", "/css/*.css?", "/js/*.js", "/js/*.js$", "/js/*.js?"],
            disallow: ["/?cat=*", "/?s=*", "/*.gif$", "/*.pdf$", "/*?"]
          },
          {
            userAgent: "Googlebot",
            allow: ["/*.css", "/*.js", "/*.css$", "/*.js$"]
          },
          {
            userAgent: "Googlebot-Image",
            allow: "/"
          },
          {
            userAgent: "Adsbot-Google",
            allow: "/"
          },
          {
            userAgent: "Googlebot-Mobile",
            allow: "/"
          },
          {
            userAgent: "noxtrumbot",
            crawlDelay: 20
          },
          {
            userAgent: "msnbot",
            crawlDelay: 20
          },
          {
            userAgent: "Slurp",
            crawlDelay: 20
          },
          {
            userAgent: "MSIECrawler",
            disallow: "/"
          },
          {
            userAgent: "WebCopier",
            disallow: "/"
          },
          {
            userAgent: "HTTrack",
            disallow: "/"
          },
          {
            userAgent: "Microsoft.URL.Control",
            disallow: "/"
          },
          {
            userAgent: "libwww",
            disallow: "/"
          },
          {
            userAgent: "Orthogaffe",
            disallow: "/"
          },
          {
            userAgent: "UbiCrawler",
            disallow: "/"
          },
          {
            userAgent: "DOC",
            disallow: "/"
          },
          {
            userAgent: "Zao",
            disallow: "/"
          },
          {
            userAgent: "sitecheck.internetseer.com",
            disallow: "/"
          },
          {
            userAgent: "Zealbot",
            disallow: "/"
          },
          {
            userAgent: "MSIECrawler",
            disallow: "/"
          },
          {
            userAgent: "SiteSnagger",
            disallow: "/"
          },
          {
            userAgent: "WebStripper",
            disallow: "/"
          },
          {
            userAgent: "WebCopier",
            disallow: "/"
          },
          {
            userAgent: "Fetch",
            disallow: "/"
          },
          {
            userAgent: "Offline Explorer",
            disallow: "/"
          },
          {
            userAgent: "Teleport",
            disallow: "/"
          },
          {
            userAgent: "TeleportPro",
            disallow: "/"
          },
          {
            userAgent: "WebZIP",
            disallow: "/"
          },
          {
            userAgent: "linko",
            disallow: "/"
          },
          {
            userAgent: "Xenu",
            disallow: "/"
          },
          {
            userAgent: "larbin",
            disallow: "/"
          },
          {
            userAgent: "ZyBORG",
            disallow: "/"
          },
          {
            userAgent: "Download Ninja",
            disallow: "/"
          },
          {
            userAgent: "wget",
            disallow: "/"
          },
          {
            userAgent: "grub-client",
            disallow: "/"
          },
          {
            userAgent: "k2spider",
            disallow: "/"
          },
          {
            userAgent: "NPBot",
            disallow: "/"
          },
          {
            userAgent: "WebReaper",
            disallow: "/"
          },
        ],
      },
    },
    {
      resolve: 'gatsby-plugin-matomo',
      options: {
        siteId: '1',
        matomoUrl: 'https://fluidattacks.matomo.cloud',
        siteUrl: 'https://fluidattacks.com',
      }
    },
    "gatsby-plugin-image",
    "gatsby-plugin-react-helmet",
    "gatsby-plugin-preload-fonts",
    "gatsby-plugin-sharp",
    "gatsby-plugin-styled-components",
    "gatsby-transformer-sharp",
  ],
};
