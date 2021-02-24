module.exports = {
  title: 'Fluid Attacks Documentation',
  tagline: 'Here you can find documentation for all our products',
  url: 'https://doc.fluidattacks.com',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'fluidattacks',
  projectName: 'product',
  themeConfig: {
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: true,
    },
    navbar: {
      logo: {
        alt: 'Fluid Attacks Logo',
        src: 'img/logo.png',
      },
      items: [
        {
          to: 'app/',
          activeBasePath: 'app/',
          label: 'App',
          position: 'left',
        },
        {
          to: 'asserts/',
          activeBasePath: 'asserts/',
          label: 'Asserts',
          position: 'left',
        },
        {
          to: 'machine/',
          activeBasePath: 'machine/',
          label: 'Machine',
          position: 'left',
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
              label: 'App',
              to: 'https://integrates.fluidattacks.com',
            },
            {
              label: 'Website',
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
