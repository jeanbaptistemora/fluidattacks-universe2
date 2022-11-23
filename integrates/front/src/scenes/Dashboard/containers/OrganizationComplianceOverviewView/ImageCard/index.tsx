import type { FC } from "react";
import React from "react";

import { ImgBox } from "./styles";

import { Card } from "components/Card";

interface IImageCardProps {
  alt: string;
  src: string;
}

const ImageCard: FC<IImageCardProps> = (
  props: IImageCardProps
): JSX.Element => {
  const { alt, src } = props;

  return (
    <Card cover={true}>
      <div className={"flex flex-column h-100 justify-center "}>
        <ImgBox>
          <img alt={alt} src={src} />
        </ImgBox>
      </div>
    </Card>
  );
};
export { ImageCard };
