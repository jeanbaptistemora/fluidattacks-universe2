import React from "react";
import rd3 from "react-d3-library";
import { IGraphicProps } from "./types";

const graphic: React.FC<IGraphicProps> = (props: IGraphicProps): JSX.Element => {
  const { data, height, generator, width } = props;

  return (
    <React.StrictMode>
      <rd3.Component data={generator(data, width, height)} />
    </React.StrictMode>
  );
};

export { graphic as Graphic };
