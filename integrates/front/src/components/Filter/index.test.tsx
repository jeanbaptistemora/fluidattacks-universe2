import type { ColumnDef } from "@tanstack/react-table";
import {
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React, { useState } from "react";

import type { IFilter } from ".";
import { Filters, useFilters } from ".";
import { Table } from "components/Table";

interface IRandomData {
  color: string;
  colors: string[];
  date: string;
  name: string;
  numberrange: number;
  numbertrack: number;
}

const columns: ColumnDef<IRandomData>[] = [
  {
    accessorKey: "name",
    header: "Name",
  },
  {
    accessorKey: "numberrange",
    header: "Number Range",
  },
  {
    accessorKey: "date",
    header: "Entrance Date",
  },
  {
    accessorKey: "color",
    header: "Shirt Color",
  },
  {
    accessorKey: "numbertrack",
    header: "Track Number",
  },
];

const dataset: IRandomData[] = [
  {
    color: "blue",
    colors: ["orange", "indigo", "blue", "violet"],
    date: "2022-01-20",
    name: "Daria Hays",
    numberrange: 12,
    numbertrack: 6,
  },
  {
    color: "blue",
    colors: ["yellow", "green", "blue", "red"],
    date: "2022-06-18",
    name: "Palmer Wilcox",
    numberrange: 12,
    numbertrack: 2,
  },
  {
    color: "white",
    colors: ["green", "orange", "blue"],
    date: "2023-01-22",
    name: "Merritt Sherman",
    numberrange: 13,
    numbertrack: 3,
  },
  {
    color: "white",
    colors: ["indigo", "green"],
    date: "2022-08-28",
    name: "Forrest Ortiz",
    numberrange: 7,
    numbertrack: 1,
  },
  {
    color: "red",
    colors: ["blue"],
    date: "2023-08-19",
    name: "April Long",
    numberrange: 6,
    numbertrack: 6,
  },
  {
    color: "red",
    colors: ["orange", "violet", "green"],
    date: "2022-06-20",
    name: "Desirae Bailey",
    numberrange: 9,
    numbertrack: 2,
  },
  {
    color: "brown",
    colors: ["green", "yellow", "violet", "indigo", "blue"],
    date: "2023-03-31",
    name: "Kato Soto",
    numberrange: 11,
    numbertrack: 2,
  },
  {
    color: "brown",
    colors: ["blue", "indigo", "red", "yellow"],
    date: "2023-07-08",
    name: "Emerald Brennan",
    numberrange: 11,
    numbertrack: 6,
  },
  {
    color: "black",
    colors: ["red", "green", "yellow", "blue", "orange"],
    date: "2022-05-12",
    name: "Donovan Woods",
    numberrange: 9,
    numbertrack: 8,
  },
  {
    color: "black",
    colors: ["violet", "indigo", "yellow", "orange", "blue"],
    date: "2022-03-07",
    name: "Brandon Hernandez",
    numberrange: 6,
    numbertrack: 0,
  },
  {
    color: "blue",
    colors: ["violet", "orange"],
    date: "2023-08-23",
    name: "Phyllis Garrett",
    numberrange: 11,
    numbertrack: 9,
  },
  {
    color: "blue",
    colors: ["brown", "orange", "black", "white"],
    date: "2022-06-29",
    name: "Theodore Daniels",
    numberrange: 9,
    numbertrack: 10,
  },
  {
    color: "white",
    colors: ["red"],
    date: "2023-08-28",
    name: "Coby Delgado",
    numberrange: 12,
    numbertrack: 13,
  },
  {
    color: "white",
    colors: ["white", "black"],
    date: "2023-06-12",
    name: "Lareina Shaffer",
    numberrange: 14,
    numbertrack: 6,
  },
  {
    color: "red",
    colors: [],
    date: "2023-04-16",
    name: "Arthur Richardson",
    numberrange: 12,
    numbertrack: 1,
  },
  {
    color: "red",
    colors: ["orange"],
    date: "2021-07-30",
    name: "Amber Morgan",
    numberrange: 8,
    numbertrack: 3,
  },
  {
    color: "brown",
    colors: ["violet", "black"],
    date: "2021-01-26",
    name: "Justin Clay",
    numberrange: 10,
    numbertrack: 3,
  },
  {
    color: "brown",
    colors: ["yellow", "red", "aquamarine"],
    date: "2023-04-01",
    name: "Timothy Powers",
    numberrange: 0,
    numbertrack: 2,
  },
  {
    color: "black",
    colors: ["yellow", "lemon"],
    date: "2022-03-24",
    name: "Marshall Massey",
    numberrange: 7,
    numbertrack: 7,
  },
  {
    color: "black",
    colors: ["deep blue", "blue", "violet", "aquamarine"],
    date: "2023-05-29",
    name: "Brian Reeves",
    numberrange: 1,
    numbertrack: 5,
  },
  {
    color: "blue",
    colors: ["deep blue", "red"],
    date: "2022-10-19",
    name: "Lesley Howard",
    numberrange: 7,
    numbertrack: 9,
  },
  {
    color: "blue",
    colors: ["yellow", "blue"],
    date: "2022-06-24",
    name: "Ivor Delgado",
    numberrange: 1,
    numbertrack: 0,
  },
  {
    color: "white",
    colors: ["lemon", "orange", "white", "deep blue", "aquamarine"],
    date: "2022-08-17",
    name: "Leila William",
    numberrange: 7,
    numbertrack: 4,
  },
  {
    color: "white",
    colors: ["transparent", "aquamarine", "chocolate", "deep blue"],
    date: "2023-05-12",
    name: "Steel Dominguez",
    numberrange: 5,
    numbertrack: 8,
  },
  {
    color: "red",
    colors: ["indigo"],
    date: "2023-02-09",
    name: "Beau Vaughn",
    numberrange: 14,
    numbertrack: 3,
  },
  {
    color: "red",
    colors: ["aquamarine", "yellow", "lemon", "chocolate"],
    date: "2022-08-04",
    name: "Mannix Bradley",
    numberrange: 15,
    numbertrack: 4,
  },
  {
    color: "brown",
    colors: ["orange", "red", "yellow", "transparent"],
    date: "2023-07-15",
    name: "Dean Zimmerman",
    numberrange: 6,
    numbertrack: 2,
  },
];

interface ITestComponentProps {
  data: IRandomData[];
  filters: IFilter<IRandomData>[];
}

const TestComponent: React.FC<ITestComponentProps> = ({
  data,
  filters,
}): JSX.Element => {
  const [filterHelper, setFilterHelper] =
    useState<IFilter<IRandomData>[]>(filters);

  const filteredData = useFilters(data, filterHelper);

  return (
    <React.Fragment>
      <Filters filters={filterHelper} setFilters={setFilterHelper} />
      <Table
        columns={columns}
        data={filteredData}
        enableSearchBar={false}
        id={"testTable"}
      />
    </React.Fragment>
  );
};

describe("Filters", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Filters).toBe("function");
  });

  it("should display and test button", async (): Promise<void> => {
    expect.hasAssertions();

    const filters: IFilter<IRandomData>[] = [];

    render(<TestComponent data={dataset} filters={filters} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Filter" }));

    expect(
      screen.getByRole("button", { name: "Clear filters" })
    ).toBeInTheDocument();

    expect(
      within(document.querySelectorAll(`aside`)[0]).getByRole("button", {
        name: "",
      })
    ).toBeInTheDocument();

    await userEvent.click(
      within(document.querySelectorAll(`aside`)[0]).getByRole("button", {
        name: "",
      })
    );

    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();
  });

  it("should mantain many filters", async (): Promise<void> => {
    expect.hasAssertions();

    const filters: IFilter<IRandomData>[] = [
      {
        id: "numberrange",
        key: "numberrange",
        label: "Number Range",
        type: "numberRange",
      },
      {
        id: "color",
        key: "color",
        label: "Color",
        selectOptions: [...new Set(dataset.map((item): string => item.color))],
        type: "select",
      },
    ];

    render(<TestComponent data={dataset} filters={filters} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Filter" }));

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("spinbutton", { name: "numberrange" })
      ).toHaveLength(2);
    });

    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "color" })
      ).toBeInTheDocument();
    });

    fireEvent.change(screen.getByRole("combobox", { name: "color" }), {
      target: { value: "blue" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(7);
    });

    fireEvent.change(
      screen.getAllByRole("spinbutton", { name: "numberrange" })[0],
      {
        target: { value: "7" },
      }
    );

    fireEvent.change(
      screen.getAllByRole("spinbutton", { name: "numberrange" })[1],
      {
        target: { value: "7" },
      }
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });

    fireEvent.change(screen.getByRole("combobox", { name: "color" }), {
      target: { value: "red" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter text", async (): Promise<void> => {
    expect.hasAssertions();

    const filters: IFilter<IRandomData>[] = [
      { id: "name", key: "name", label: "Name", type: "text" },
    ];

    render(<TestComponent data={dataset} filters={filters} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Filter" }));

    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "name" })
      ).toBeInTheDocument();
    });

    await userEvent.type(
      screen.getByRole("textbox", { name: "name" }),
      "lareina shaffer"
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter text case sensitive", async (): Promise<void> => {
    expect.hasAssertions();

    const filters: IFilter<IRandomData>[] = [
      {
        filterFn: "caseSensitive",
        id: "name",
        key: "name",
        label: "Name",
        type: "text",
      },
    ];

    render(<TestComponent data={dataset} filters={filters} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Filter" }));

    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "name" })
      ).toBeInTheDocument();
    });

    await userEvent.type(
      screen.getByRole("textbox", { name: "name" }),
      "lareina shaffer"
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });

    await userEvent.click(
      screen.getByRole("button", { name: "Clear filters" })
    );

    await userEvent.type(
      screen.getByRole("textbox", { name: "name" }),
      "Lareina Shaffer"
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter text includes case insensitive", async (): Promise<void> => {
    expect.hasAssertions();

    const filters: IFilter<IRandomData>[] = [
      {
        filterFn: "includesInsensitive",
        id: "name",
        key: "name",
        label: "Name",
        type: "text",
      },
    ];

    render(<TestComponent data={dataset} filters={filters} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Filter" }));

    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "name" })
      ).toBeInTheDocument();
    });

    await userEvent.type(
      screen.getByRole("textbox", { name: "name" }),
      "lareina shaf"
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter text includes case sensitive", async (): Promise<void> => {
    expect.hasAssertions();

    const filters: IFilter<IRandomData>[] = [
      {
        filterFn: "includesSensitive",
        id: "name",
        key: "name",
        label: "Name",
        type: "text",
      },
    ];

    render(<TestComponent data={dataset} filters={filters} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Filter" }));

    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "name" })
      ).toBeInTheDocument();
    });

    await userEvent.type(
      screen.getByRole("textbox", { name: "name" }),
      "lareina shaf"
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });

    await userEvent.click(
      screen.getByRole("button", { name: "Clear filters" })
    );

    await userEvent.type(
      screen.getByRole("textbox", { name: "name" }),
      "Lareina Shaf"
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter number", async (): Promise<void> => {
    expect.hasAssertions();

    const filters: IFilter<IRandomData>[] = [
      {
        id: "numbertrack",
        key: "numbertrack",
        label: "Number Track",
        type: "number",
      },
    ];

    render(<TestComponent data={dataset} filters={filters} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Filter" }));

    await waitFor((): void => {
      expect(
        screen.queryByRole("spinbutton", { name: "numbertrack" })
      ).toBeInTheDocument();
    });

    fireEvent.change(screen.getByRole("spinbutton", { name: "numbertrack" }), {
      target: { value: "8" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(3);
    });
  });

  it("should filter number range", async (): Promise<void> => {
    expect.hasAssertions();

    const filters: IFilter<IRandomData>[] = [
      {
        id: "numberrange",
        key: "numberrange",
        label: "Number Range",
        type: "numberRange",
      },
    ];

    render(<TestComponent data={dataset} filters={filters} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Filter" }));

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("spinbutton", { name: "numberrange" })
      ).toHaveLength(2);
    });

    fireEvent.change(
      screen.getAllByRole("spinbutton", { name: "numberrange" })[0],
      {
        target: { value: "1" },
      }
    );

    fireEvent.change(
      screen.getAllByRole("spinbutton", { name: "numberrange" })[1],
      {
        target: { value: "5" },
      }
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(4);
    });
  });

  it("should filter date range", async (): Promise<void> => {
    expect.hasAssertions();

    const filters: IFilter<IRandomData>[] = [
      {
        id: "date",
        key: "date",
        label: "Date Range",
        type: "dateRange",
      },
    ];

    render(<TestComponent data={dataset} filters={filters} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Filter" }));

    await waitFor((): void => {
      expect(document.querySelectorAll(`input[name="date"]`)).toHaveLength(2);
    });

    fireEvent.change(document.querySelectorAll(`input[name="date"]`)[0], {
      target: { value: "2021-01-01" },
    });

    fireEvent.change(document.querySelectorAll(`input[name="date"]`)[1], {
      target: { value: "2022-03-31" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(6);
    });
  });

  it("should filter select", async (): Promise<void> => {
    expect.hasAssertions();

    const filters: IFilter<IRandomData>[] = [
      {
        id: "color",
        key: "color",
        label: "Color",
        selectOptions: [
          ...new Set(dataset.map((item): string => item.color)),
        ].map((entry): { header: string; value: string } => {
          return { header: entry, value: entry };
        }),
        type: "select",
      },
    ];

    render(<TestComponent data={dataset} filters={filters} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Filter" }));

    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "color" })
      ).toBeInTheDocument();
    });

    fireEvent.change(screen.getByRole("combobox", { name: "color" }), {
      target: { value: "red" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(7);
    });
  });

  it("should filter includes in array", async (): Promise<void> => {
    expect.hasAssertions();

    const filters: IFilter<IRandomData>[] = [
      {
        filterFn: "includesInArray",
        id: "colors",
        key: "colors",
        label: "Colors",
        selectOptions: [
          "red",
          "orange",
          "yellow",
          "green",
          "blue",
          "indigo",
          "violet",
          "white",
          "brown",
          "black",
          "aquamarine",
          "deep blue",
          "chocolate",
          "transparent",
        ],
        type: "select",
      },
    ];

    render(<TestComponent data={dataset} filters={filters} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Filter" }));

    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "colors" })
      ).toBeInTheDocument();
    });

    fireEvent.change(screen.getByRole("combobox", { name: "colors" }), {
      target: { value: "transparent" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(3);
    });
  });

  it("should filter custom", async (): Promise<void> => {
    expect.hasAssertions();

    function customFilterFn(data: IRandomData): boolean {
      return data.color === "brown";
    }

    const filters: IFilter<IRandomData>[] = [
      { id: "name", key: customFilterFn, label: "name" },
    ];

    render(<TestComponent data={dataset} filters={filters} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Filter" })).toBeInTheDocument();

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(6);
    });
  });
});
