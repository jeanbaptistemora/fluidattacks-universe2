module.exports = {
  pathPrefix: '/new-front',
  siteMetadata: {
    title: "A Pentesting Company | Fluid Attacks",
    description:
      "We're a pentesting and ethical hacking company that identifies and \
      reports all your applications and software vulnerabilities ASAP.",
    url: "https://fluidattacks.com/new-front", // No trailing slash allowed!
    image: "/images/logo-fluid-attacks.png", // Path to your image you placed in the 'static' folder
  },
  plugins: [
    {
      resolve: "gatsby-plugin-manifest",
      options: {
        name: "Fluid Attacks",
        short_name: "https://fluidattacks.com",
        start_url: "/",
        background_color: "#ffffff",
        theme_color: "#663399",
        display: "minimal-ui",
        icon: "src/images/favicon.png", // This path is relative to the root of the site.,
      },
    },
    {
      resolve: 'gatsby-plugin-web-font-loader',
      options: {
        google: {
          families: ["Roboto:300,400,700,900"]
        }
      }
    },
    {
      resolve: "gatsby-source-filesystem",
      options: {
        path: "../content/pages",
        name: 'pages',
      },
    },
    {
      resolve: "gatsby-transformer-asciidoc",
      options: {
        attributes: {
          showtitle: true,
        },
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
      resolve: "gatsby-plugin-breadcrumb",
      options: {
        // useAutoGen: required 'true' to use autogen
        useAutoGen: true,
        // autoGenHomeLabel: optional 'Home' is default
        // exlude: optional, include this array to exclude paths you don't want to
        // generate breadcrumbs for (see below for details).
        // isMatchOptions: optional, include this object to configure the wildcard-match library.
        excludeOptions: {
          separator: '.'
        },
        // crumbLabelUpdates: optional, update specific crumbLabels in the path
        // trailingSlashes: optional, will add trailing slashes to the end
        // of crumb pathnames. default is false
        trailingSlashes: true,
        // usePathPrefix: optional, if you are using pathPrefix above
        usePathPrefix: "/new-front",
     },
    },
    "gatsby-plugin-remove-trailing-slashes",
    "gatsby-plugin-react-helmet",
    "gatsby-transformer-asciidoc",
    "gatsby-plugin-styled-components",
    "gatsby-plugin-typescript",
    "gatsby-transformer-sharp",
    "gatsby-plugin-sass",
  ],
}
