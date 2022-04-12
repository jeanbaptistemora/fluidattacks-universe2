/* eslint import/no-namespace:0 */
/* eslint @typescript-eslint/no-non-null-assertion:0 */
import React from "react";
import { Helmet } from "react-helmet";

interface ISeoProps {
  title: string;
  description: string;
  image: string;
  url: string;
}

const ServiceSeo: React.FC<ISeoProps> = ({
  title,
  description,
  image,
  url,
}: ISeoProps): JSX.Element => {
  return (
    <Helmet>
      <script type={"application/ld+json"}>{`
        {
          "@context": "https://schema.org/",
          "@type": "Service",
          "name": "${title}",
          "image": "${image}",
          "description": "${description}",
          "brand": {
            "@type": "Brand",
            "name": "Fluid Attacks"
          },
          "offers": {
            "@type": "Offer",
            "url": "${url}"
          }
        }
    `}</script>
    </Helmet>
  );
};

export { ServiceSeo };
