import type { ColumnDef } from "@tanstack/react-table";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { vulnerabilityFormatter } from "./vulnerabilityFormat";

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
    where?: string;
    specific?: string;
    verification?: string;
    vulnerabilityType?: string;
    treatment?: string;
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
    {
      currentState: "App",
    },
    {
      currentState: "Code",
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

    await userEvent.click(screen.getByText("19"));

    expect(screen.queryAllByRole("row")).toHaveLength(20);
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

    await userEvent.click(screen.getByText("19"));

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

    expect(screen.getByText("App")).toBeInTheDocument();
    expect(screen.getByText("App")).toHaveStyle(
      `background-color: ${variants.blue.bgColor};
      border: 1px solid ${variants.blue.borderColor};
      color: ${variants.blue.color};`
    );

    expect(screen.getByText("Code")).toBeInTheDocument();
    expect(screen.getByText("Code")).toHaveStyle(
      `background-color: ${variants.blue.bgColor};
      border: 1px solid ${variants.blue.borderColor};
      color: ${variants.blue.color};`
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

    await userEvent.click(screen.getByText("19"));

    expect(screen.queryByText("Pending verification")).not.toBeInTheDocument();
    expect(screen.queryByText("Permanently accepted")).not.toBeInTheDocument();
    expect(screen.queryByText("Temporarily accepted")).not.toBeInTheDocument();
    expect(screen.queryByText("Should be gray")).not.toBeInTheDocument();
    expect(screen.queryByText("Verified (closed)")).not.toBeInTheDocument();
    expect(screen.queryByText("Verified (open)")).not.toBeInTheDocument();
  });

  it("should have a long text in complete status format", async (): Promise<void> => {
    expect.hasAssertions();

    const columnsCompleteStatus: ColumnDef<IRandomData>[] = [
      {
        accessorKey: "currentState",
        cell: (cell): JSX.Element => statusFormatter(cell.getValue(), true),
        header: "Status",
      },
    ];

    render(
      <Table
        columns={columnsCompleteStatus}
        data={data}
        enableColumnFilters={true}
        id={"testTable"}
      />
    );

    expect(screen.getByRole("table")).toBeInTheDocument();

    await userEvent.click(screen.getByText("19"));

    expect(screen.getByText("Pending verification")).toBeInTheDocument();
    expect(screen.getByText("Permanently accepted")).toBeInTheDocument();
    expect(screen.getByText("Temporarily accepted")).toBeInTheDocument();
    expect(screen.getByText("Should be gray")).toBeInTheDocument();
    expect(screen.getByText("Verified (closed)")).toBeInTheDocument();
    expect(screen.getByText("Verified (open)")).toBeInTheDocument();
  });

  it("should have complete status format", async (): Promise<void> => {
    expect.hasAssertions();

    const columnsCompleteStatus: ColumnDef<IRandomData>[] = [
      {
        accessorKey: "currentState",
        cell: (cell): JSX.Element => statusFormatter(cell.getValue(), true),
        header: "Status",
      },
    ];

    render(
      <Table
        columns={columnsCompleteStatus}
        data={data}
        enableColumnFilters={true}
        id={"testTable"}
      />
    );

    expect(screen.getByRole("table")).toBeInTheDocument();

    await userEvent.click(screen.getByText("19"));

    expect(screen.getByText("Closed")).toBeInTheDocument();
    expect(screen.getByText("Closed")).toHaveStyle(
      `background-color: ${variants.green.bgColor};
      border: 1px solid ${variants.green.borderColor};
      color: ${variants.green.color};`
    );

    expect(screen.getByText("Should be gray")).toBeInTheDocument();
    expect(screen.getByText("Should be gray")).toHaveStyle(
      `background-color: ${variants.gray.bgColor};
      border: 1px solid ${variants.gray.borderColor};
      color: ${variants.gray.color};`
    );

    expect(screen.getByText("N/a")).toBeInTheDocument();
    expect(screen.getByText("N/a")).toHaveStyle(
      `background-color: ${variants.gray.bgColor};
      border: 1px solid ${variants.gray.borderColor};
      color: ${variants.gray.color};`
    );

    expect(screen.getByText("On hold")).toBeInTheDocument();
    expect(screen.getByText("On hold")).toHaveStyle(
      `background-color: ${variants.orange.bgColor};
      border: 1px solid ${variants.orange.borderColor};
      color: ${variants.orange.color};`
    );

    expect(screen.getByText("Pending verification")).toBeInTheDocument();
    expect(screen.getByText("Pending verification")).toHaveStyle(
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

  it("should not have value on complete status", (): void => {
    expect.hasAssertions();

    const columnsCompleteStatus: ColumnDef<IRandomData>[] = [
      {
        accessorKey: "currentState",
        cell: (cell): JSX.Element => statusFormatter(cell.getValue(), true),
        header: "Status",
      },
    ];

    const dataCompleteStatus: IRandomData[] = [
      {
        currentState: "-",
      },
    ];

    render(
      <Table
        columns={columnsCompleteStatus}
        data={dataCompleteStatus}
        enableColumnFilters={true}
        id={"testTable"}
      />
    );

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.queryAllByRole("row")).toHaveLength(2);
    expect(screen.queryByText("-")).not.toBeInTheDocument();
  });

  it("should not have gray color in format", async (): Promise<void> => {
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

    await userEvent.click(screen.getByText("19"));

    expect(screen.queryByText("Code")).not.toHaveStyle(
      `background-color: ${variants.gray.bgColor};
      border: 1px solid ${variants.gray.borderColor};
      color: ${variants.gray.color};`
    );
    expect(screen.queryByText("Closed")).not.toHaveStyle(
      `background-color: ${variants.gray.bgColor};
      border: 1px solid ${variants.gray.borderColor};
      color: ${variants.gray.color};`
    );
    expect(screen.queryByText("Open")).not.toHaveStyle(
      `background-color: ${variants.gray.bgColor};
      border: 1px solid ${variants.gray.borderColor};
      color: ${variants.gray.color};`
    );
    expect(screen.queryByText("Pending")).not.toHaveStyle(
      `background-color: ${variants.gray.bgColor};
      border: 1px solid ${variants.gray.borderColor};
      color: ${variants.gray.color};`
    );

    jest.clearAllMocks();
  });

  it("should have vulnerability format", (): void => {
    expect.hasAssertions();

    const vulnColumns: ColumnDef<IRandomData>[] = [
      {
        accessorKey: "where",
        cell: (cell): JSX.Element =>
          vulnerabilityFormatter({
            reattack: cell.row.original.verification,
            source: cell.row.original.vulnerabilityType,
            specific: cell.row.original.specific as string,
            status: cell.row.original.currentState,
            treatment: cell.row.original.treatment,
            where: cell.getValue(),
          }),
        header: "Vulnerability",
      },
    ];

    const vulnData: IRandomData[] = [
      {
        currentState: "closed",
        specific: "here",
        treatment: "New",
        verification: "Requested",
        vulnerabilityType: "Infra",
        where: "testing",
      },
      {
        currentState: "open",
        specific: "here",
        verification: "Masked",
        vulnerabilityType: "Code",
        where: "testing2",
      },
      {
        currentState: "closed",
        specific: "here",
        treatment: "In progress",
        vulnerabilityType: "App",
        where: "testing3",
      },
      {
        currentState: "open",
        specific: "here",
        vulnerabilityType: "App",
        where: "testing4",
      },
      {
        currentState: "open",
        specific: "here",
        treatment: "Untreated",
        vulnerabilityType: "App",
        where: "testing5",
      },
    ];

    render(
      <Table
        columns={vulnColumns}
        data={vulnData}
        enableColumnFilters={true}
        id={"testTable"}
      />
    );

    expect(screen.getByRole("table")).toBeInTheDocument();
    expect(screen.getByText("testing | here")).toBeInTheDocument();

    expect(screen.getAllByText("Vulnerable")[0]).toBeInTheDocument();
    expect(screen.getAllByText("Vulnerable")[0]).toHaveStyle(
      `background-color: ${variants.red.bgColor};
      border: 1px solid ${variants.red.borderColor};
      color: ${variants.red.color};`
    );

    expect(screen.getAllByText("Safe")[0]).toBeInTheDocument();
    expect(screen.getAllByText("Safe")[0]).toHaveStyle(
      `background-color: ${variants.green.bgColor};
      border: 1px solid ${variants.green.borderColor};
      color: ${variants.green.color};`
    );

    expect(screen.getByText("Infra")).toBeInTheDocument();
    expect(screen.getByText("Infra")).toHaveStyle(
      `background-color: ${variants.blue.bgColor};
      border: 1px solid ${variants.blue.borderColor};
      color: ${variants.blue.color};`
    );

    expect(screen.getByText("Code")).toBeInTheDocument();
    expect(screen.getByText("Code")).toHaveStyle(
      `background-color: ${variants.blue.bgColor};
      border: 1px solid ${variants.blue.borderColor};
      color: ${variants.blue.color};`
    );

    expect(screen.getAllByText("App")[0]).toBeInTheDocument();
    expect(screen.getAllByText("App")[0]).toHaveStyle(
      `background-color: ${variants.blue.bgColor};
      border: 1px solid ${variants.blue.borderColor};
      color: ${variants.blue.color};`
    );

    expect(screen.getByText("Requested")).toBeInTheDocument();
    expect(screen.getByText("Requested")).toHaveStyle(
      `background-color: ${variants.orange.bgColor};
      border: 1px solid ${variants.orange.borderColor};
      color: ${variants.orange.color};`
    );

    expect(screen.getByText("New")).toBeInTheDocument();
    expect(screen.getByText("New")).toHaveStyle(
      `background-color: ${variants.orange.bgColor};
      border: 1px solid ${variants.orange.borderColor};
      color: ${variants.orange.color};`
    );

    expect(screen.getByText("In progress")).toBeInTheDocument();
    expect(screen.getByText("In progress")).toHaveStyle(
      `background-color: ${variants.orange.bgColor};
      border: 1px solid ${variants.orange.borderColor};
      color: ${variants.orange.color};`
    );

    expect(screen.getByText("Masked")).toBeInTheDocument();
    expect(screen.getByText("Masked")).toHaveStyle(
      `background-color: ${variants.orange.bgColor};
      border: 1px solid ${variants.orange.borderColor};
      color: ${variants.orange.color};`
    );

    expect(screen.getByText("Untreated")).toBeInTheDocument();
    expect(screen.getByText("Untreated")).toHaveStyle(
      `background-color: ${variants.orange.bgColor};
      border: 1px solid ${variants.orange.borderColor};
      color: ${variants.orange.color};`
    );
  });
});
