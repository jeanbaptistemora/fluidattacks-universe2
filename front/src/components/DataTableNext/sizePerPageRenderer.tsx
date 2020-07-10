import React from "react";
import { DropdownButton, MenuItem } from "react-bootstrap";

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
        id={"pageSizeDropDown"}
        onSelect={handleSelect}
        title={currSizePerPage}
      >
        {options.map(
          (option: Readonly<{ page: number; text: string }>): JSX.Element => (
            <MenuItem eventKey={option.page} key={option.text}>
              {option.page}
            </MenuItem>
          )
        )}
      </DropdownButton>
    </div>
  );
};
