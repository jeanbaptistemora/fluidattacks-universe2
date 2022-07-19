import React from "react";
import type { SizePerPageRendererOptions } from "react-bootstrap-table-next";

import { Button } from "components/Button";

const SizePerPageRenderer: (props: SizePerPageRendererOptions) => JSX.Element =
  ({
    options,
    currSizePerPage,
    onSizePerPageChange,
  }: Readonly<SizePerPageRendererOptions>): JSX.Element => (
    <span>
      {options.map(
        ({ page, text }): JSX.Element => (
          <Button
            key={text}
            onClick={function handleClick(): void {
              onSizePerPageChange(page);
            }}
            size={"sm"}
            variant={currSizePerPage === text ? "secondary" : "ghost"}
          >
            {text}
          </Button>
        )
      )}
    </span>
  );

export { SizePerPageRenderer };
