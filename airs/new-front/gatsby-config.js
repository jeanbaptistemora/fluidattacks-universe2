module.exports = {
  siteMetadata: {
    title: "A Pentesting Company | Fluid Attacks",
    description:
      "We're a pentesting and ethical hacking company that identifies and \
      reports all your applications and software vulnerabilities ASAP.",
    url: "https://fluidattacks.com/new-front", // No trailing slash allowed!
    image: "/images/fluid-attacks-logo.webp", // Path to your image you placed in the 'static' folder
  },
  plugins: [
    {
      resolve: "gatsby-plugin-canonical-urls",
      options: {
        siteUrl: "https://fluidattacks.com",
      },
    },
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
    "gatsby-plugin-react-helmet",
    "gatsby-plugin-styled-components",
    "gatsby-plugin-typescript",
    "gatsby-transformer-sharp",
    "gatsby-plugin-sass",
  ],
}
