module.exports = {
  title: 'Fluid Attacks Documentation',
  tagline: 'Here you can find documentation for all our products',
  url: 'https://docs.fluidattacks.com',
  baseUrl: process.env.env == 'prod' ? '/' : `/${process.env.CI_COMMIT_REF_NAME}/`,
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'throw',
  favicon: 'img/favicon.ico',
  organizationName: 'fluidattacks',
  projectName: 'product',
  themeConfig: {
    googleAnalytics: {
      trackingID: 'GTM-PCDDL8T',
      anonymizeIP: true,
    },
    colorMode: {
      defaultMode: 'light',
      disableSwitch: true,
    },
    navbar: {
      logo: {
        alt: 'Fluid Attacks Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          to: 'about/faq',
          activeBasePath: 'about/',
          label: 'About',
          position: 'left',
        },
        {
          to: 'machine/app',
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
          sidebarPath: require.resolve('./sidebars.js'),
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
};
