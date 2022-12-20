/* eslint camelcase: 0 */
/* eslint @typescript-eslint/no-confusing-void-expression: 0 */
/* eslint react/require-default-props: 0 */
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

const CloudImage: React.FC<{
  alt: string;
  isProfile?: boolean;
  src: string;
  styles?: string;
}> = ({ alt, isProfile = false, src, styles }): JSX.Element => {
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

  const defaultImage = (
    <img
      alt={"default"}
      src={
        "https://res.cloudinary.com/fluid-attacks/image/upload/v1671487952/airs/blogs/authors/default.png"
      }
    />
  );

  const imageElements = data.allCloudinaryMedia.edges
    .filter((image): boolean => image.node.secure_url.includes(src))
    .map(
      (image: IImageNode): JSX.Element => (
        <img
          alt={alt}
          className={styles}
          key={alt}
          src={image.node.secure_url.replace(".png", ".webp")}
        />
      )
    );

  if (imageElements.length < 1 && isProfile) {
    return defaultImage;
  } else if (imageElements.length < 1) {
    return <p>{"Image not found"}</p>;
  }

  return <React.StrictMode>{imageElements}</React.StrictMode>;
};

export { CloudImage };
