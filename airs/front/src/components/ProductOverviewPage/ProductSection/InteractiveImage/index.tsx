import React, { useCallback, useState } from "react";

import { Container } from "./styledComponents";

import { CloudImage } from "../../../CloudImage";
import { HotSpotButton } from "../../../HotSpotButton";

interface IInteractiveProps {
  hasHotSpot: boolean;
  image1: string;
  image2: string;
  isRight: boolean;
}

const InteractiveImage: React.FC<IInteractiveProps> = ({
  hasHotSpot,
  image1,
  image2,
  isRight,
}: IInteractiveProps): JSX.Element => {
  const [isTouch, setIsTouch] = useState(false);

  const onClick = useCallback((): void => {
    setIsTouch(!isTouch);
  }, [isTouch]);

  return (
    <Container>
      {hasHotSpot ? (
        <HotSpotButton
          id={image1}
          isRight={isRight}
          onClick={onClick}
          tooltipMessage={"Click to view"}
        />
      ) : undefined}
      <CloudImage
        alt={"Image Demo"}
        src={isTouch ? image2 : image1}
        styles={`bs-product-image ${hasHotSpot ? "mt0" : "mt4"}`}
      />
    </Container>
  );
};

export { InteractiveImage };
