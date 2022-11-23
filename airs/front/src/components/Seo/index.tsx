/* eslint import/no-namespace:0 */
/* eslint @typescript-eslint/no-non-null-assertion:0 */
import { string } from "prop-types"; // eslint-disable-line import/default
import React from "react";
import { Helmet } from "react-helmet";

interface IMetaItem {
  content: string;
  name: string;
  property?: string;
}

interface ILinkItem {
  href: string;
  rel: string;
}

interface ISeoProps {
  title?: string;
  description?: string;
  url?: string;
  author?: string;
  keywords?: string;
  meta?: IMetaItem[];
  image?: string;
}

const Seo: React.FC<ISeoProps> = ({
  title,
  description,
  url,
  author,
  keywords,
  meta,
  image,
}: ISeoProps): JSX.Element => {
  const siteTitle: string = title!;
  const siteDescription: string = description!;
  const siteUrl: string = url!;
  const siteAuthor: string = author!;
  const siteImage: string = image!;
  const siteKeywords: string = keywords!;
  const metaData: IMetaItem[] = [
    {
      content: siteAuthor,
      name: "author",
    },
    {
      content: siteUrl,
      name: "canonical",
    },
    {
      content: siteDescription,
      name: "description",
    },
    {
      content: siteImage,
      name: "image",
      property: "og:image",
    },
    {
      content: siteUrl,
      name: "og:url",
    },
    {
      content: "article",
      name: "og:type",
    },
    {
      content: siteTitle,
      name: "og:title",
    },
    {
      content: siteDescription,
      name: "og:description",
    },
    {
      content: siteImage,
      name: "og:image",
    },
    {
      content: "summary_large_image",
      name: "twitter:card",
    },
    {
      content: siteAuthor,
      name: "twitter:creator",
    },
    {
      content: siteTitle,
      name: "twitter:title",
    },
    {
      content: siteDescription,
      name: "twitter:description",
    },
    {
      content: siteImage,
      name: "twitter:image",
    },
    {
      content: siteKeywords,
      name: "keywords",
    },
  ].concat(meta!);

  const linkData: ILinkItem[] = [
    {
      href: "https://res.cloudinary.com/fluid-attacks/image/upload/v1619036532/airs/favicon_bkgq2p.webp",
      rel: "shortcut icon",
    },
  ];

  return (
    <Helmet
      htmlAttributes={{ lang: "en" }}
      link={linkData}
      meta={metaData}
      title={siteTitle}
    />
  );
};

// eslint-disable-next-line fp/no-mutation
Seo.propTypes = {
  author: string,
  description: string,
  image: string,
  keywords: string,
  title: string,
  url: string,
};

// eslint-disable-next-line fp/no-mutation
Seo.defaultProps = {
  author: "",
  description: "",
  image: "",
  keywords: "",
  meta: [
    {
      content: "",
      name: "",
    },
  ],
  title: "",
  url: "",
};

export { Seo };
