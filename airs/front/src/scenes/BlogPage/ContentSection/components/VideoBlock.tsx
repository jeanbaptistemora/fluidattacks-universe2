import React from "react";

import { VideoBlockContainer } from "./styledComponents";

interface IVideoProps {
  children: React.ReactNode;
}

const VideoBlock: React.FC<IVideoProps> = ({ children }): JSX.Element => (
  <VideoBlockContainer>{children}</VideoBlockContainer>
);

export { VideoBlock };
