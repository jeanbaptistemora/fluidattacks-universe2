module.exports = {
  title: 'Fluid Attacks Documentation',
  tagline: 'Here you can find documentation for all our products',
  url: 'https://docs.fluidattacks.com',
  baseUrl: process.env.env == 'prod' ? '/' : `/${process.env.branch}/`,
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'throw',
  favicon: 'https://res.cloudinary.com/fluid-attacks/image/upload/v1622211888/docs/favicon_be6154.ico',
  organizationName: 'fluidattacks',
  projectName: 'product',
  themeConfig: {
    matomo: {
      matomoUrl: 'https://fluidattacks.matomo.cloud/',
      siteId: '2',
    },
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
    },
    navbar: {
      logo: {
        alt: 'Fluid Attacks Logo',
        src: 'https://res.cloudinary.com/fluid-attacks/image/upload/v1622577821/docs/logo_gyivrl.svg',
        srcDark: 'https://res.cloudinary.com/fluid-attacks/image/upload/v1623782670/docs/logo_dark_esf1gn.svg',
      },
      items: [
        {
          to: 'about/faq',
          activeBasePath: 'about/',
          label: 'About',
          position: 'left',
        },
        {
          to: 'machine/web',
          activeBasePath: 'machine/',
          label: 'Machine',
          position: 'left',
        },
        {
          to: 'squad',
          activeBasePath: 'squad/',
          label: 'Squad',
          position: 'left',
        },
        {
          to: 'criteria/',
          activeBasePath: 'criteria/',
          label: 'Criteria',
          position: 'left',
        },
        {
          to: 'development/',
          activeBasePath: 'development/',
          label: 'Development',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Community',
          items: [
            {
              label: 'Discord',
              href: 'https://community.fluidattacks.com',
            },
            {
              label: 'Help',
              href: 'https://help.fluidattacks.com',
            },
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/company/fluidattacks',
            },
          ],
        },
        {
          title: 'Main',
          items: [
            {
              label: 'Web',
              to: 'https://app.fluidattacks.com',
            },
            {
              label: 'Site',
              to: 'https://fluidattacks.com',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: 'https://fluidattacks.com/blog',
            },
            {
              label: 'Gitlab',
              href: 'https://gitlab.com/fluidattacks/product',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Fluid Attacks, We hack your software. All rights reserved.`,
    },
    prism: {
      theme: require('prism-react-renderer/themes/oceanicNext'),
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebar.js'),
          routeBasePath: '/',
        },
        blog: {
          showReadingTime: true,
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
  plugins: [
    [ require.resolve('docusaurus-gtm-plugin'), { id: 'GTM-PCDDL8T' } ],
    require.resolve('docusaurus-lunr-search'),
    require.resolve('docusaurus-plugin-matomo'),
  ],
};
