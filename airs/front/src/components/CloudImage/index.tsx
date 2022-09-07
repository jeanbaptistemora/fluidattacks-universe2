/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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

const CloudImage: React.FC<{ alt: string; src: string; styles?: string }> = ({
  alt,
  src,
  styles,
}: {
  alt: string;
  src: string;
  styles?: string;
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
        <img
          alt={alt}
          className={styles}
          key={alt}
          src={image.node.secure_url.replace(".png", ".webp")}
        />
      )
    );

  return (
    <React.StrictMode>
      {imageElements.length < 1 ? <p>{"Image not found"}</p> : imageElements}
    </React.StrictMode>
  );
};

export { CloudImage };
