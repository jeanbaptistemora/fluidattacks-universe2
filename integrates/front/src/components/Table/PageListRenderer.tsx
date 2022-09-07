/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";
import type { PageListRendererOptions } from "react-bootstrap-table-next";

import { Button } from "components/Button";

const PageListRenderer: (props: PageListRendererOptions) => JSX.Element = ({
  onPageChange,
  pages,
}: Readonly<PageListRendererOptions>): JSX.Element => (
  <span>
    {pages.map(
      ({ active, page }): JSX.Element => (
        <Button
          key={page}
          onClick={function handleClick(): void {
            onPageChange(page, 10);
          }}
          size={"sm"}
          variant={active ? "secondary" : "ghost"}
        >
          {page}
        </Button>
      )
    )}
  </span>
);

export { PageListRenderer };
