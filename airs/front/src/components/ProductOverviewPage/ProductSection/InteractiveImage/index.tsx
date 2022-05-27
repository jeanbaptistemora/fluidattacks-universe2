import React, { useState } from "react";

import { Container } from "./styledComponents";

import { CloudImage } from "../../../CloudImage";
import { HotSpotButton } from "../../../HotSpotButton";

interface IInteractiveProps {
  image1: string;
  image2: string;
  isRight: boolean;
}

const InteractiveImage: React.FC<IInteractiveProps> = ({
  image1,
  image2,
  isRight,
}: IInteractiveProps): JSX.Element => {
  const [isTouch, setIsTouch] = useState(false);

  function onClick(): void {
    setIsTouch(!isTouch);
  }

  return (
    <Container>
      <HotSpotButton isRight={isRight} onClick={onClick} />
      <CloudImage
        alt={"Image Demo"}
        src={isTouch ? image2 : image1}
        styles={"bs-product-image"}
      />
    </Container>
  );
};

export { InteractiveImage };
