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
    "gatsby-plugin-react-helmet",
    "gatsby-transformer-asciidoc",
    "gatsby-plugin-styled-components",
    "gatsby-plugin-typescript",
    "gatsby-transformer-sharp",
    "gatsby-plugin-sass",
  ],
}
