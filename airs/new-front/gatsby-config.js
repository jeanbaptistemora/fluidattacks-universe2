module.exports = {
  siteMetadata: {
    title: "A Pentesting Company | Fluid Attacks",
    description:
      "We're a pentesting and ethical hacking company that identifies and \
      reports all your applications and software vulnerabilities ASAP.",
    url: "https://fluidattacks.com/new-front", // No trailing slash allowed!
    image: "/images/fluid-attacks-logo.png", // Path to your image you placed in the 'static' folder
  },
  plugins: [
    `gatsby-plugin-react-helmet`,
    `gatsby-plugin-typescript`,
  ],
}
