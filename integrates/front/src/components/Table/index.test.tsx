import type { ColumnDef, Row } from "@tanstack/react-table";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React, { useState } from "react";

import { Table } from "components/Table";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";

interface IRandomData {
  color: string;
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
  {
    accessorKey: "numbertrack",
    header: "Track Number",
    meta: { filterType: "number" },
  },
];

const data: IRandomData[] = [
  {
    color: "blue",
    date: "2022-01-20",
    name: "Daria Hays",
    numberrange: 12,
    numbertrack: 6,
  },
  {
    color: "blue",
    date: "2022-06-18",
    name: "Palmer Wilcox",
    numberrange: 12,
    numbertrack: 2,
  },
  {
    color: "white",
    date: "2023-01-22",
    name: "Merritt Sherman",
    numberrange: 13,
    numbertrack: 3,
  },
  {
    color: "white",
    date: "2022-08-28",
    name: "Forrest Ortiz",
    numberrange: 7,
    numbertrack: 1,
  },
  {
    color: "red",
    date: "2023-08-19",
    name: "April Long",
    numberrange: 6,
    numbertrack: 6,
  },
  {
    color: "red",
    date: "2022-06-20",
    name: "Desirae Bailey",
    numberrange: 9,
    numbertrack: 2,
  },
  {
    color: "brown",
    date: "2023-03-31",
    name: "Kato Soto",
    numberrange: 11,
    numbertrack: 2,
  },
  {
    color: "brown",
    date: "2023-07-08",
    name: "Emerald Brennan",
    numberrange: 11,
    numbertrack: 6,
  },
  {
    color: "black",
    date: "2022-05-12",
    name: "Donovan Woods",
    numberrange: 9,
    numbertrack: 8,
  },
  {
    color: "black",
    date: "2022-03-07",
    name: "Brandon Hernandez",
    numberrange: 6,
    numbertrack: 0,
  },
  {
    color: "blue",
    date: "2023-08-23",
    name: "Phyllis Garrett",
    numberrange: 11,
    numbertrack: 9,
  },
  {
    color: "blue",
    date: "2022-06-29",
    name: "Theodore Daniels",
    numberrange: 9,
    numbertrack: 10,
  },
  {
    color: "white",
    date: "2023-08-28",
    name: "Coby Delgado",
    numberrange: 12,
    numbertrack: 13,
  },
  {
    color: "white",
    date: "2023-06-12",
    name: "Lareina Shaffer",
    numberrange: 14,
    numbertrack: 6,
  },
  {
    color: "red",
    date: "2023-04-16",
    name: "Arthur Richardson",
    numberrange: 12,
    numbertrack: 1,
  },
  {
    color: "red",
    date: "2021-07-30",
    name: "Amber Morgan",
    numberrange: 8,
    numbertrack: 3,
  },
  {
    color: "brown",
    date: "2021-01-26",
    name: "Justin Clay",
    numberrange: 10,
    numbertrack: 3,
  },
  {
    color: "brown",
    date: "2023-04-01",
    name: "Timothy Powers",
    numberrange: 0,
    numbertrack: 2,
  },
  {
    color: "black",
    date: "2022-03-24",
    name: "Marshall Massey",
    numberrange: 7,
    numbertrack: 7,
  },
  {
    color: "black",
    date: "2023-05-29",
    name: "Brian Reeves",
    numberrange: 1,
    numbertrack: 5,
  },
  {
    color: "blue",
    date: "2022-10-19",
    name: "Lesley Howard",
    numberrange: 7,
    numbertrack: 9,
  },
  {
    color: "blue",
    date: "2022-06-24",
    name: "Ivor Delgado",
    numberrange: 1,
    numbertrack: 0,
  },
  {
    color: "white",
    date: "2022-08-17",
    name: "Leila William",
    numberrange: 7,
    numbertrack: 4,
  },
  {
    color: "white",
    date: "2023-05-12",
    name: "Steel Dominguez",
    numberrange: 5,
    numbertrack: 8,
  },
  {
    color: "red",
    date: "2023-02-09",
    name: "Beau Vaughn",
    numberrange: 14,
    numbertrack: 3,
  },
  {
    color: "red",
    date: "2022-08-04",
    name: "Mannix Bradley",
    numberrange: 15,
    numbertrack: 4,
  },
  {
    color: "brown",
    date: "2023-07-15",
    name: "Dean Zimmerman",
    numberrange: 6,
    numbertrack: 2,
  },
];

describe("Table", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Table).toBe("function");
  });

  it("should render csv button", (): void => {
    expect.hasAssertions();

    render(
      <Table columns={columns} data={data} exportCsv={true} id={"testTable"} />
    );

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "group.findings.exportCsv.text" })
    ).toBeInTheDocument();
  });

  it("should filter numberRange upper bound", async (): Promise<void> => {
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

    await userEvent.click(screen.queryAllByRole("button")[0]);

    fireEvent.change(
      screen.queryAllByRole("spinbutton", { name: "numberrange" })[1],
      { target: { value: "5" } }
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(5);
    });

    await userEvent.click(
      screen.getByRole("button", { name: "Clear filters" })
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(11);
    });
  });

  it("should filter numberRange lower bound", async (): Promise<void> => {
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

    await userEvent.click(screen.queryAllByRole("button")[0]);

    fireEvent.change(
      screen.queryAllByRole("spinbutton", { name: "numberrange" })[0],
      { target: { value: "14" } }
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(4);
    });

    await userEvent.click(
      screen.getByRole("button", { name: "Clear filters" })
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(11);
    });
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
    expect(screen.queryAllByRole("row")).toHaveLength(11);

    await userEvent.click(screen.queryAllByRole("button")[0]);

    fireEvent.change(screen.getByRole("combobox", { name: "color" }), {
      target: { value: "red" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(7);
    });

    await userEvent.click(
      screen.getByRole("button", { name: "Clear filters" })
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(11);
    });
  });

  it("should filter text", async (): Promise<void> => {
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

    await userEvent.click(screen.queryAllByRole("button")[0]);

    fireEvent.change(screen.getByRole("textbox", { name: "name" }), {
      target: { value: "lareina shaffer" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });

    await userEvent.click(
      screen.getByRole("button", { name: "Clear filters" })
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(11);
    });
  });

  it("should filter dateRange lower bound", async (): Promise<void> => {
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

    await userEvent.click(screen.queryAllByRole("button")[0]);

    expect(
      document.querySelectorAll(`input[name="date"]`)[0]
    ).toBeInTheDocument();

    fireEvent.change(document.querySelectorAll(`input[name="date"]`)[0], {
      target: { value: "2023-08-01" },
    });
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(4);
    });

    expect(screen.queryByText("April Long")).toBeInTheDocument();
    expect(screen.queryByText("Desirae Bailey")).not.toBeInTheDocument();

    await userEvent.click(
      screen.getByRole("button", { name: "Clear filters" })
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(11);
    });
  });

  it("should filter dateRange upper bound", async (): Promise<void> => {
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

    await userEvent.click(screen.queryAllByRole("button")[0]);

    expect(
      document.querySelectorAll(`input[name="date"]`)[1]
    ).toBeInTheDocument();

    fireEvent.change(document.querySelectorAll(`input[name="date"]`)[1], {
      target: { value: "2021-12-01" },
    });
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(3);
    });

    expect(screen.queryByText("Amber Morgan")).toBeInTheDocument();
    expect(screen.queryByText("Desirae Bailey")).not.toBeInTheDocument();

    await userEvent.click(
      screen.getByRole("button", { name: "Clear filters" })
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(11);
    });
  });

  it("should not render pagination", (): void => {
    expect.hasAssertions();

    render(
      <Table
        columns={columns}
        data={data.slice(0, 10)}
        enableColumnFilters={true}
        id={"testTable"}
      />
    );

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.queryAllByRole("row")).toHaveLength(11);

    expect(
      screen.queryByRole("button", { name: "10" })
    ).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "1" })).not.toBeInTheDocument();
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

    await userEvent.click(screen.getByRole("button", { name: "20" }));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(21);
    });

    await userEvent.click(screen.getByRole("button", { name: "27" }));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(28);
    });

    await userEvent.click(screen.getByRole("button", { name: "10" }));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(11);
    });

    await userEvent.click(screen.getByRole("button", { name: "3" }));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(8);
    });

    await userEvent.click(screen.getByRole("button", { name: "1" }));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(11);
    });

    expect(screen.queryByText("Daria Hays")).toBeInTheDocument();

    void userEvent.click(screen.getAllByRole("button", { name: "" })[1]);
    await waitFor((): void => {
      expect(screen.queryByText("Phyllis Garrett")).toBeInTheDocument();
    });

    expect(screen.queryByText("Daria Hays")).not.toBeInTheDocument();

    void userEvent.click(screen.getAllByRole("button", { name: "" })[0]);
    await waitFor((): void => {
      expect(screen.queryByText("Daria Hays")).toBeInTheDocument();
    });

    expect(screen.queryByText("Phyllis Garrett")).not.toBeInTheDocument();

    void userEvent.click(screen.getAllByRole("button", { name: "" })[1]);
    await waitFor((): void => {
      expect(screen.queryByText("Theodore Daniels")).toBeInTheDocument();
    });

    void userEvent.click(screen.getAllByRole("button", { name: "" })[1]);
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(8);
    });

    await userEvent.click(screen.getByRole("button", { name: "1" }));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(11);
    });

    expect(screen.queryByText("Daria Hays")).toBeInTheDocument();
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

    await userEvent.click(
      screen.getByRole("button", { name: "group.findings.tableSet.btn.text" })
    );
    await waitFor((): void => {
      expect(
        screen.getByText("group.findings.tableSet.modalTitle")
      ).toBeInTheDocument();
    });

    expect(screen.getAllByRole("checkbox")).toHaveLength(5);

    await userEvent.click(screen.getByRole("checkbox", { name: "color" }));

    expect(
      screen.queryByRole("columnheader", { name: "Shirt Color" })
    ).not.toBeInTheDocument();

    await userEvent.click(screen.getByRole("checkbox", { name: "color" }));

    expect(
      screen.queryByRole("columnheader", { name: "Shirt Color" })
    ).toBeInTheDocument();
  });

  it("should sort data", async (): Promise<void> => {
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
      screen.getByRole("columnheader", { name: "Name" })
    ).toBeInTheDocument();

    expect(screen.queryAllByRole("cell")[0].textContent).toBe("Daria Hays");

    await userEvent.click(screen.getByRole("columnheader", { name: "Name" }));

    await waitFor((): void => {
      expect(screen.queryAllByRole("cell")[0].textContent).toBe("Amber Morgan");
    });

    await userEvent.click(screen.getByRole("columnheader", { name: "Name" }));

    await waitFor((): void => {
      expect(screen.queryAllByRole("cell")[0].textContent).toBe(
        "Timothy Powers"
      );
    });

    await userEvent.click(screen.getByRole("columnheader", { name: "Name" }));

    await waitFor((): void => {
      expect(screen.queryAllByRole("cell")[0].textContent).toBe("Daria Hays");
    });
  });

  interface ITestComponentProps {
    TData: IRandomData[];
    expandedRow?: (row: Row<IRandomData>) => JSX.Element;
    selectionMode?: "checkbox" | "radio";
  }

  const TestComponent: React.FC<ITestComponentProps> = ({
    expandedRow,
    selectionMode,
    TData,
  }): JSX.Element => {
    const [selectedData, setSelectedData] = useState<IRandomData[]>([]);

    return (
      <React.Fragment>
        <p>{JSON.stringify(selectedData[0])}</p>
        <Table
          columns={columns}
          data={TData}
          expandedRow={expandedRow}
          id={"testTable"}
          rowSelectionSetter={setSelectedData}
          rowSelectionState={selectedData}
          selectionMode={selectionMode}
        />
      </React.Fragment>
    );
  };

  it("should only select one when radio selection", async (): Promise<void> => {
    expect.hasAssertions();

    render(<TestComponent TData={data} selectionMode={"radio"} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.queryAllByRole("radio", { checked: true })).toHaveLength(0);

    await userEvent.click(screen.queryAllByRole("radio")[0]);
    await waitFor((): void => {
      expect(
        screen.getByText(
          `{"color":"blue","date":"2022-01-20","name":"Daria Hays","numberrange":12,"numbertrack":6}`
        )
      ).toBeInTheDocument();
    });

    expect(screen.queryAllByRole("radio", { checked: true })).toHaveLength(1);

    await userEvent.click(screen.queryAllByRole("radio")[1]);
    await waitFor((): void => {
      expect(
        screen.getByText(
          `{"color":"blue","date":"2022-06-18","name":"Palmer Wilcox","numberrange":12,"numbertrack":2}`
        )
      ).toBeInTheDocument();
    });

    expect(screen.queryAllByRole("radio", { checked: true })).toHaveLength(1);
  });

  it("should select all checkboxes", async (): Promise<void> => {
    expect.hasAssertions();

    render(<TestComponent TData={data} selectionMode={"checkbox"} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
      0
    );

    await userEvent.click(screen.queryAllByRole("checkbox")[0]);
    await waitFor((): void => {
      expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
        11
      );
    });

    await userEvent.click(screen.queryAllByRole("checkbox")[0]);
    await waitFor((): void => {
      expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
        0
      );
    });
  });

  it("should select many checkboxes", async (): Promise<void> => {
    expect.hasAssertions();

    render(<TestComponent TData={data} selectionMode={"checkbox"} />);

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
      0
    );

    await userEvent.click(screen.queryAllByRole("checkbox")[1]);
    await waitFor((): void => {
      expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
        2
      );
    });

    await userEvent.click(screen.queryAllByRole("checkbox")[2]);
    await waitFor((): void => {
      expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
        3
      );
    });

    await userEvent.click(screen.queryAllByRole("checkbox")[3]);
    await waitFor((): void => {
      expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
        4
      );
    });
  });

  function handleRowExpand(row: Row<IRandomData>): JSX.Element {
    return <p>{`This is ${row.original.name} expanded`}</p>;
  }

  it("should expand rows", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      // eslint-disable-next-line
      <TestComponent TData={data.slice(0, 2)} expandedRow={handleRowExpand} /> // NOSONAR
    );

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(
      screen.queryByText("This is Daria Hays expanded")
    ).not.toBeInTheDocument();
    expect(
      screen.queryByText("This is Palmer Wilcox expanded")
    ).not.toBeInTheDocument();

    await userEvent.click(screen.queryAllByRole("button", { name: "" })[1]);
    await waitFor((): void => {
      expect(
        screen.queryByText("This is Daria Hays expanded")
      ).toBeInTheDocument();
      expect(
        screen.queryByText("This is Palmer Wilcox expanded")
      ).not.toBeInTheDocument();
    });
    await userEvent.click(screen.queryAllByRole("button", { name: "" })[2]);
    await waitFor((): void => {
      expect(
        screen.queryByText("This is Daria Hays expanded")
      ).toBeInTheDocument();
      expect(
        screen.queryByText("This is Palmer Wilcox expanded")
      ).toBeInTheDocument();
    });
    await userEvent.click(screen.queryAllByRole("button", { name: "" })[0]);
    await userEvent.click(screen.queryAllByRole("button", { name: "" })[0]);
    await waitFor((): void => {
      expect(
        screen.queryByText("This is Daria Hays expanded")
      ).not.toBeInTheDocument();
      expect(
        screen.queryByText("This is Palmer Wilcox expanded")
      ).not.toBeInTheDocument();
    });
    await userEvent.click(screen.queryAllByRole("button", { name: "" })[0]);
    await waitFor((): void => {
      expect(
        screen.queryByText("This is Daria Hays expanded")
      ).toBeInTheDocument();
      expect(
        screen.queryByText("This is Palmer Wilcox expanded")
      ).toBeInTheDocument();
    });
  });
});
