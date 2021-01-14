import React from "react";
import { DropdownButton, MenuItem } from "components/DropdownButton";

export const SizePerPageRenderer: React.FC<SizePerPageRenderer> = (
  // Readonly utility type doesn't seem to work on SizePerPageRenderer
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: SizePerPageRenderer
): JSX.Element => {
  const { options, currSizePerPage, onSizePerPageChange } = props;
  function handleSelect(select: unknown): void {
    onSizePerPageChange(select as number);
  }

  return (
    <div>
      <DropdownButton
        content={currSizePerPage}
        id={"pageSizeDropDown"}
        items={options.map(
          (option: Readonly<{ page: number; text: string }>): JSX.Element => (
            <MenuItem
              eventKey={`${option.page}`}
              itemContent={option.page}
              key={option.text}
              onClick={handleSelect}
            />
          )
        )}
        width={"sizePageDropdownBtn"}
      />
    </div>
  );
};
