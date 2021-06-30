import React from "react";

import { DropdownButton, MenuItem } from "components/DropdownButton";

export interface ISizePerPageProps {
  currSizePerPage: number;
  onSizePerPageChange: (page: number) => void;
  options: { page: number; text: string }[];
}

export const SizePerPageRenderer = (props: ISizePerPageProps): JSX.Element => {
  const { options, currSizePerPage, onSizePerPageChange } = props;
  function handleSelect(select: unknown): void {
    onSizePerPageChange(select as number);
  }

  return (
    <DropdownButton
      content={currSizePerPage}
      id={"pageSizeDropDown"}
      items={options.map(
        (option): JSX.Element => (
          <MenuItem
            eventKey={`${option.page}`}
            itemContent={option.page}
            key={option.text}
            onClick={handleSelect}
          />
        )
      )}
      scrollInto={true}
    />
  );
};
