import React from "react";

import style from "components/DataTableNext/index.css";

export interface ISizePerPageProps {
  currSizePerPage: number;
  onSizePerPageChange: (page: number) => void;
  options: { page: number; text: string }[];
}

export const SizePerPageRenderer = (props: ISizePerPageProps): JSX.Element => {
  const { options, currSizePerPage, onSizePerPageChange } = props;

  return (
    <div>
      {options.map((option): JSX.Element => {
        const isSelect = `${currSizePerPage}` === option.text;
        function handleClick(): void {
          onSizePerPageChange(option.page);
        }

        return (
          <button
            className={`${
              isSelect ? style.selectedSizePerPage : style.sizePerPage
            }`}
            key={option.text}
            onClick={handleClick}
          >
            {option.text}
          </button>
        );
      })}
    </div>
  );
};
