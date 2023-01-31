import React, { Fragment, useState } from "react";

import { Buttons } from "./styles";

interface IContentSwitcherProps {
  contents: JSX.Element[];
  initSelection?: number;
  tabs: string[];
}

const ContentSwitcher: React.FC<IContentSwitcherProps> = ({
  contents,
  initSelection = 0,
  tabs,
}: Readonly<IContentSwitcherProps>): JSX.Element => {
  const [selection, setSelection] = useState(initSelection);
  const handleClicks: (() => void)[] = tabs.map(
    (_, idx): (() => void) =>
      (): void => {
        setSelection(idx);
      }
  );

  return (
    <Fragment>
      <Buttons>
        {tabs.map(
          (el: string, idx): JSX.Element => (
            <button
              className={selection === idx ? "active" : undefined}
              key={el}
              onClick={handleClicks[idx]}
            >
              {el}
            </button>
          )
        )}
      </Buttons>
      {contents[selection]}
    </Fragment>
  );
};

export type { IContentSwitcherProps };
export { ContentSwitcher };
