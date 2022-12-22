import React from "react";

import { ImageBlockContainer } from "./styledComponents";

interface IImageProps {
  children: React.ReactNode;
}

const ImageBlock: React.FC<IImageProps> = ({ children }): JSX.Element => (
  <ImageBlockContainer>{children}</ImageBlockContainer>
);

export { ImageBlock };
