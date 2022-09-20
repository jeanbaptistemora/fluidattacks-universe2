/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ColumnDef } from "@tanstack/react-table";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { Table } from "components/TableNew";
import { filterDate } from "components/TableNew/filters/filterFunctions/filterDate";

interface IRandomData {
  color: string;
  date: string;
  name: string;
  numberrange: number;
}

const columns: ColumnDef<IRandomData>[] = [
  {
    accessorKey: "name",
    header: "Name",
  },
  {
    accessorKey: "numberrange",
    header: "Number Range",
    meta: { filterType: "numberRange" },
  },
  {
    accessorKey: "date",
    filterFn: filterDate,
    header: "Entrance Date",
    meta: { filterType: "dateRange" },
  },
  {
    accessorKey: "color",
    header: "Shirt Color",
    meta: { filterType: "select" },
  },
];

const data: IRandomData[] = [
  {
    color: "blue",
    date: "2022-01-20",
    name: "Daria Hays",
    numberrange: 12,
  },
  {
    color: "blue",
    date: "2022-06-18",
    name: "Palmer Wilcox",
    numberrange: 12,
  },
  {
    color: "white",
    date: "2023-01-22",
    name: "Merritt Sherman",
    numberrange: 13,
  },
  {
    color: "white",
    date: "2022-08-28",
    name: "Forrest Ortiz",
    numberrange: 7,
  },
  {
    color: "red",
    date: "2023-08-19",
    name: "April Long",
    numberrange: 6,
  },
  {
    color: "red",
    date: "2022-06-20",
    name: "Desirae Bailey",
    numberrange: 9,
  },
  {
    color: "brown",
    date: "2023-03-31",
    name: "Kato Soto",
    numberrange: 11,
  },
  {
    color: "brown",
    date: "2023-07-08",
    name: "Emerald Brennan",
    numberrange: 11,
  },
  {
    color: "black",
    date: "2022-05-12",
    name: "Donovan Woods",
    numberrange: 9,
  },
  {
    color: "black",
    date: "2022-03-07",
    name: "Brandon Hernandez",
    numberrange: 6,
  },
  {
    color: "blue",
    date: "2023-08-23",
    name: "Phyllis Garrett",
    numberrange: 11,
  },
  {
    color: "blue",
    date: "2022-06-29",
    name: "Theodore Daniels",
    numberrange: 9,
  },
  {
    color: "white",
    date: "2023-08-28",
    name: "Coby Delgado",
    numberrange: 12,
  },
  {
    color: "white",
    date: "2023-06-12",
    name: "Lareina Shaffer",
    numberrange: 14,
  },
  {
    color: "red",
    date: "2023-04-16",
    name: "Arthur Richardson",
    numberrange: 12,
  },
  {
    color: "red",
    date: "2021-07-30",
    name: "Amber Morgan",
    numberrange: 8,
  },
  {
    color: "brown",
    date: "2021-01-26",
    name: "Justin Clay",
    numberrange: 10,
  },
  {
    color: "brown",
    date: "2023-04-01",
    name: "Timothy Powers",
    numberrange: 0,
  },
  {
    color: "black",
    date: "2022-03-24",
    name: "Marshall Massey",
    numberrange: 7,
  },
  {
    color: "black",
    date: "2023-05-29",
    name: "Brian Reeves",
    numberrange: 1,
  },
  {
    color: "blue",
    date: "2022-10-19",
    name: "Lesley Howard",
    numberrange: 7,
  },
  {
    color: "blue",
    date: "2022-06-24",
    name: "Ivor Delgado",
    numberrange: 1,
  },
  {
    color: "white",
    date: "2022-08-17",
    name: "Leila William",
    numberrange: 7,
  },
  {
    color: "white",
    date: "2023-05-12",
    name: "Steel Dominguez",
    numberrange: 5,
  },
  {
    color: "red",
    date: "2023-02-09",
    name: "Beau Vaughn",
    numberrange: 14,
  },
  {
    color: "red",
    date: "2022-08-04",
    name: "Mannix Bradley",
    numberrange: 15,
  },
  {
    color: "brown",
    date: "2023-07-15",
    name: "Dean Zimmerman",
    numberrange: 6,
  },
];

describe("Table", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Table).toBe("function");
  });

  it("should filter table", async (): Promise<void> => {
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
    expect(screen.queryAllByRole("row")).toHaveLength(11);

    userEvent.click(screen.queryAllByRole("button")[0]);

    fireEvent.change(screen.getByPlaceholderText("Min"), {
      target: { value: "12" },
    });
    fireEvent.change(screen.getByPlaceholderText("Max"), {
      target: { value: "15" },
    });
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(9);
    });
    userEvent.click(screen.getByRole("button", { name: "Clear filters" }));

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(11);
    });

    fireEvent.change(screen.getByRole("combobox", { name: "color" }), {
      target: { value: "red" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(7);
    });
  });

  it("should change pagination", async (): Promise<void> => {
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
    expect(screen.queryAllByRole("row")).toHaveLength(11);

    userEvent.click(screen.getByRole("button", { name: "20" }));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(21);
    });

    userEvent.click(screen.getByRole("button", { name: "27" }));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(28);
    });

    userEvent.click(screen.getByRole("button", { name: "10" }));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(11);
    });

    userEvent.click(screen.getByRole("button", { name: "3" }));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(8);
    });
  });

  it("should hide columns", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <Table
        columnToggle={true}
        columns={columns}
        data={data}
        id={"testTable"}
      />
    );

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "group.findings.tableSet.btn.text" })
    ).toBeInTheDocument();

    expect(
      screen.getByRole("columnheader", { name: "Shirt Color" })
    ).toBeInTheDocument();

    userEvent.click(
      screen.getByRole("button", { name: "group.findings.tableSet.btn.text" })
    );
    await waitFor((): void => {
      expect(
        screen.getByText("group.findings.tableSet.modalTitle")
      ).toBeInTheDocument();
    });

    expect(screen.getAllByRole("checkbox")).toHaveLength(4);

    userEvent.click(screen.getByRole("checkbox", { name: "color" }));

    expect(
      screen.queryByRole("columnheader", { name: "Shirt Color" })
    ).not.toBeInTheDocument();

    userEvent.click(screen.getByRole("checkbox", { name: "color" }));

    expect(
      screen.queryByRole("columnheader", { name: "Shirt Color" })
    ).toBeInTheDocument();
  });
});
