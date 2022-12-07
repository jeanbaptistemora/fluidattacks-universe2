import React, { Fragment, useState } from "react";

import { Buttons } from "./styles";

import { Button } from "components/Button";

interface ICarouselProps {
  contents: JSX.Element[];
  initSelection?: number;
  tabs: string[];
}

const Carousel: React.FC<ICarouselProps> = ({
  contents,
  initSelection = 0,
  tabs,
}: Readonly<ICarouselProps>): JSX.Element => {
  const [selection, setSelection] = useState(initSelection);
  const handleClicks: (() => void)[] = tabs.map(
    (_, idx): (() => void) =>
      (): void => {
        setSelection(idx);
      }
  );

  return (
    <Fragment>
      {contents[selection]}
      <Buttons selection={selection}>
        {tabs.map(
          (el: string, idx): JSX.Element => (
            <Button
              key={el}
              onClick={handleClicks[idx]}
              size={"xxs"}
              variant={"carousel"}
            >
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
