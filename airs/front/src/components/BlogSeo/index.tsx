/* eslint import/no-namespace:0 */
/* eslint @typescript-eslint/no-non-null-assertion:0 */
import { string } from "prop-types"; // eslint-disable-line import/default
import React from "react";
import { Helmet } from "react-helmet";

interface ISeoProps {
  title?: string;
  date?: string;
  description?: string;
  url?: string;
  author?: string;
  image?: string;
}

const BlogSeo: React.FC<ISeoProps> = ({
  title,
  date,
  description,
  url,
  author,
  image,
}: ISeoProps): JSX.Element => {
  const siteTitle: string = title!;
  const siteDate: string = date!;
  const siteDescription: string = description!;
  const siteUrl: string = url!;
  const siteAuthor: string = author!;
  const siteImage: string = image!;

  return (
    <Helmet>
      <script type={"application/ld+json"}>{`
          "@context": "https://schema.org/",
          "@type": "Article",
          "author": "${siteAuthor}",
          "headline": "${siteTitle}",
          "image": "${siteImage}",
          "datePublished": "${siteDate}",
          "publisher": {
            "@type": "Organization",
            "name": "Fluid Attacks",
            "logo": {
              "@type": "ImageObject",
              "url": "https://res.cloudinary.com/fluid-attacks/image/upload/q_auto,f_auto/v1622583388/airs/logo_fluid_attacks_2021_eqop3k.svg"
            },
            "address": "95 3rd St, 2nd Floor",
            "location": "San Francisco, CA, 94107, Estados Unidos"
          },
          "dateModified": "${siteDate}",
          "mainEntityOfPage": "${siteUrl}",
          "description": "${siteDescription}"
    `}</script>
    </Helmet>
  );
};

// eslint-disable-next-line fp/no-mutation
BlogSeo.propTypes = {
  author: string,
  date: string,
  description: string,
  image: string,
  title: string,
  url: string,
};

// eslint-disable-next-line fp/no-mutation
BlogSeo.defaultProps = {
  author: "",
  date: "",
  description: "",
  image: "",
  title: "",
  url: "",
};

export { BlogSeo };
