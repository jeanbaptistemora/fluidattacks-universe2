/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ColumnDef } from "@tanstack/react-table";
import { render, screen } from "@testing-library/react";
import React from "react";

import { Table } from "components/Table";
import { formatState } from "scenes/Dashboard/containers/GroupFindingsView/utils";

describe("Formatter", (): void => {
  interface IRandomData {
    currentState: string;
  }

  const columns: ColumnDef<IRandomData>[] = [
    {
      accessorKey: "currentState",
      cell: (cell): JSX.Element => formatState(cell.getValue()),
      header: "Status",
    },
  ];

  const data: IRandomData[] = [
    {
      currentState: "Open",
    },
    {
      currentState: "Closed",
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Table).toBe("function");
  });

  it("should filter select", (): void => {
    expect.hasAssertions();

    render(
      <Table
        columns={columns}
        data={data}
        enableColumnFilters={true}
        id={"testTable"}
      />
    );

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.queryAllByRole("row")).toHaveLength(3);
  });
});
