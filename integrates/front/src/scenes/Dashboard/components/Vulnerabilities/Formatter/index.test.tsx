/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ColumnDef } from "@tanstack/react-table";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { statusFormatter } from ".";
import { Table } from "components/Table";

describe("Formatter", (): void => {
  interface IVariant {
    bgColor: string;
    borderColor: string;
    color: string;
  }

  const variants: Record<string, IVariant> = {
    blue: {
      bgColor: "#dce4f7",
      borderColor: "#3778ff",
      color: "#3778ff",
    },
    gray: {
      bgColor: "#d2d2da",
      borderColor: "#2e2e38",
      color: "#2e2e38",
    },
    green: {
      bgColor: "#c2ffd4",
      borderColor: "#009245",
      color: "#009245",
    },
    orange: {
      bgColor: "#ffeecc",
      borderColor: "#d88218",
      color: "#d88218",
    },
    red: {
      bgColor: "#fdd8da",
      borderColor: "#bf0b1a",
      color: "#bf0b1a",
    },
  };

  interface IRandomData {
    currentState: string;
  }

  const columns: ColumnDef<IRandomData>[] = [
    {
      accessorKey: "currentState",
      cell: (cell): JSX.Element => statusFormatter(cell.getValue()),
      header: "Status",
    },
  ];

  const data: IRandomData[] = [
    {
      currentState: "Active",
    },
    {
      currentState: "Closed",
    },
    {
      currentState: "OK",
    },
    {
      currentState: "Verified (closed)",
    },
    {
      currentState: "Accepted",
    },
    {
      currentState: "In progress",
    },
    {
      currentState: "New",
    },
    {
      currentState: "On_hold",
    },
    {
      currentState: "Pending verification",
    },
    {
      currentState: "Permanently accepted",
    },
    {
      currentState: "Temporarily accepted",
    },
    {
      currentState: "Disabled",
    },
    {
      currentState: "Open",
    },
    {
      currentState: "Unsolved",
    },
    {
      currentState: "Verified (open)",
    },
    {
      currentState: "N/A",
    },
    {
      currentState: "Should be gray",
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Table).toBe("function");
  });

  it("should filter select", async (): Promise<void> => {
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

    await userEvent.click(screen.getByText("17"));

    expect(screen.queryAllByRole("row")).toHaveLength(18);
  });

  it("should have status format", async (): Promise<void> => {
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

    await userEvent.click(screen.getByText("17"));

    expect(screen.getByText("Closed")).toBeInTheDocument();
    expect(screen.getByText("Closed")).toHaveStyle(
      `background-color: ${variants.green.bgColor};
      border: 1px solid ${variants.green.borderColor};
      color: ${variants.green.color};`
    );

    expect(screen.getByText("Ok")).toBeInTheDocument();
    expect(screen.getByText("Ok")).toHaveStyle(
      `background-color: ${variants.green.bgColor};
      border: 1px solid ${variants.green.borderColor};
      color: ${variants.green.color};`
    );

    expect(screen.getByText("N/a")).toBeInTheDocument();
    expect(screen.getByText("N/a")).toHaveStyle(
      `background-color: ${variants.gray.bgColor};
      border: 1px solid ${variants.gray.borderColor};
      color: ${variants.gray.color};`
    );

    expect(
      screen.getByText("searchFindings.tabVuln.onHold")
    ).toBeInTheDocument();
    expect(screen.getByText("searchFindings.tabVuln.onHold")).toHaveStyle(
      `background-color: ${variants.orange.bgColor};
      border: 1px solid ${variants.orange.borderColor};
      color: ${variants.orange.color};`
    );

    expect(screen.getByText("Pending")).toBeInTheDocument();
    expect(screen.getByText("Pending")).toHaveStyle(
      `background-color: ${variants.orange.bgColor};
      border: 1px solid ${variants.orange.borderColor};
      color: ${variants.orange.color};`
    );

    expect(screen.getByText("Open")).toBeInTheDocument();
    expect(screen.getByText("Open")).toHaveStyle(
      `background-color: ${variants.red.bgColor};
      border: 1px solid ${variants.red.borderColor};
      color: ${variants.red.color};`
    );
  });

  it("should not have a long text in status format", async (): Promise<void> => {
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

    await userEvent.click(screen.getByText("17"));

    expect(screen.queryByText("Pending verification")).not.toBeInTheDocument();
    expect(screen.queryByText("Permanently accepted")).not.toBeInTheDocument();
    expect(screen.queryByText("Temporarily accepted")).not.toBeInTheDocument();
    expect(screen.queryByText("Should be gray")).not.toBeInTheDocument();
    expect(screen.queryByText("Verified (closed)")).not.toBeInTheDocument();
    expect(screen.queryByText("Verified (open)")).not.toBeInTheDocument();
  });
});
