/* eslint camelcase: 0 */
/* eslint @typescript-eslint/no-confusing-void-expression: 0 */
/* eslint fp/no-let: 0 */
import { graphql, useStaticQuery } from "gatsby";
import React from "react";

interface IImageNode {
  node: {
    secure_url: string;
  };
}

interface IData {
  allCloudinaryMedia: {
    edges: [
      {
        node: {
          secure_url: string;
        };
      }
    ];
  };
}

const CloudImage: React.FC<{ alt: string; src: string }> = ({
  alt,
  src,
}: {
  alt: string;
  src: string;
}): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query CloudinaryImage {
      allCloudinaryMedia {
        edges {
          node {
            secure_url
          }
        }
      }
    }
  `);

  const imageElements = data.allCloudinaryMedia.edges
    .filter((image): boolean => image.node.secure_url.includes(src))
    .map(
      (image: IImageNode): JSX.Element => (
        <img alt={alt} key={alt} src={image.node.secure_url} />
      )
    );

  return (
    <React.StrictMode>
      {imageElements.length < 1 ? <p>{"Image not found"}</p> : imageElements}
    </React.StrictMode>
  );
};

export { CloudImage };
