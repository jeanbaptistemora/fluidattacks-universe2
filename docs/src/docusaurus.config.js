// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Fluid Attacks Documentation",
  tagline: "Here you can find documentation for all our products",
  url: "https://docs.fluidattacks.com",
  baseUrl: process.env.env == "prod" ? "/" : `/${process.env.branch}/`,
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "throw",
  favicon:
    "https://res.cloudinary.com/fluid-attacks/image/upload/v1622211888/docs/favicon_be6154.ico",

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebar.js"),
          routeBasePath: "/",
        },
        blog: {
          showReadingTime: true,
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      matomo: {
        matomoUrl: "https://fluidattacks.matomo.cloud/",
        siteId: "2",
      },
      colorMode: {
        defaultMode: "light",
        disableSwitch: false,
      },
      navbar: {
        logo: {
          alt: "Fluid Attacks Logo",
          src: "https://res.cloudinary.com/fluid-attacks/image/upload/v1675273694/docs/Logo_2023.svg",
          srcDark:
            "https://res.cloudinary.com/fluid-attacks/image/upload/v1675273694/docs/Logo_2023_dark.svg",
        },
        items: [
          {
            to: "about/faq",
            activeBasePath: "about/",
            label: "About",
            position: "left",
          },
          {
            to: "machine/web/arm",
            activeBasePath: "machine/web",
            label: "Machine",
            position: "left",
          },
          {
            to: "squad/reattacks",
            activeBasePath: "squad/",
            label: "Squad",
            position: "left",
          },
          {
            to: "criteria/",
            activeBasePath: "criteria/",
            label: "Criteria",
            position: "left",
          },
          {
            to: "development/",
            activeBasePath: "development/",
            label: "Development",
            position: "right",
          },
          {
            type: "html",
            position: "right",
            value:
              '<a target="_blank" rel="noopener noreferrer" href="https://fluidattacks.com/free-trial/"><button class="trial-button">Start your free trial</button></a>',
          },
        ],
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Community",
            items: [
              {
                label: "Help",
                href: "https://help.fluidattacks.tech",
              },
              {
                label: "LinkedIn",
                href: "https://www.linkedin.com/company/fluidattacks",
              },
            ],
          },
          {
            title: "Main",
            items: [
              {
                label: "Web",
                to: "https://app.fluidattacks.com",
              },
              {
                label: "Site",
                to: "https://fluidattacks.com",
              },
            ],
          },
          {
            title: "More",
            items: [
              {
                label: "Blog",
                to: "https://fluidattacks.com/blog",
              },
              {
                label: "Gitlab",
                href: "https://gitlab.com/fluidattacks/universe",
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Fluid Attacks, We hack your software. All rights reserved.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
  plugins: [
    [require.resolve("docusaurus-gtm-plugin"), { id: "GTM-PCDDL8T" }],
    require.resolve("docusaurus-lunr-search"),
    require.resolve("docusaurus-plugin-matomo"),
  ],
};

module.exports = config;
