import React, { Fragment } from "react";

import { Buttons } from "./styles";

import { useCarousel } from "../../utils/hooks";
import { Button } from "components/Button";

interface ICarouselProps {
  contents: JSX.Element[];
  initSelection?: number;
  tabs: string[];
}

const Carousel: React.FC<ICarouselProps> = ({
  contents,
  tabs,
}: Readonly<ICarouselProps>): JSX.Element => {
  const timePerProgress = 70;
  const numberOfCycles = tabs.length;
  const { cycle } = useCarousel(timePerProgress, numberOfCycles);

  return (
    <Fragment>
      {contents[cycle]}
      <Buttons selection={cycle}>
        {tabs.map(
          (el: string): JSX.Element => (
            <Button key={el} size={"xxs"} variant={"carousel"}>
              {el}
            </Button>
          )
        )}
      </Buttons>
    </Fragment>
  );
};

export type { ICarouselProps };
export { Carousel };
