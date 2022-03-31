import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { Table } from "components/Table";
import { changeFormatter, deleteFormatter } from "components/Table/formatters";
import type { IHeaderConfig, ISelectRowProps } from "components/Table/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";

describe("Table", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Table).toStrictEqual("function");
  });

  it("should render an empty table", (): void => {
    expect.hasAssertions();

    const selectionMode: ISelectRowProps = {
      clickToSelect: true,
      mode: "checkbox",
    };
    const data: Record<string, unknown>[] = [];
    const testHeaders: IHeaderConfig[] = [];
    render(
      <Table
        dataset={data}
        exportCsv={false}
        headers={testHeaders}
        id={"testTable"}
        pageSize={25}
        search={false}
        selectionMode={selectionMode}
      />
    );

    expect(screen.queryByRole("table")).not.toBeInTheDocument();
    expect(screen.queryAllByRole("columnheader")).toHaveLength(0);
  });

  it("should render dynamic headers", (): void => {
    expect.hasAssertions();

    const data: Record<string, unknown>[] = [
      {
        testHeader: "value 1",
        testHeader2: "value 2",
      },
    ];
    const selectionMode: ISelectRowProps = {
      clickToSelect: true,
      mode: "checkbox",
    };
    const testHeaders: IHeaderConfig[] = [];
    render(
      <Table
        dataset={data}
        exportCsv={false}
        headers={testHeaders}
        id={"testTable"}
        pageSize={25}
        search={false}
        selectionMode={selectionMode}
      />
    );
    const numberOfDynamicHeaders: number = 3;

    expect(screen.queryByRole("table")).toBeInTheDocument();
    expect(
      screen.queryByText("table.noDataIndication")
    ).not.toBeInTheDocument();
    expect(screen.queryAllByRole("columnheader")).toHaveLength(
      numberOfDynamicHeaders
    );
  });

  it("should render a table with id", (): void => {
    expect.hasAssertions();

    const data: Record<string, unknown>[] = [
      {
        testHeader: "value 1",
        testHeader2: "value 2",
      },
    ];
    const testHeaders: IHeaderConfig[] = [
      {
        dataField: "testHeader",
        header: "Prueba 1",
        width: "5%",
        wrapped: false,
      },
      {
        dataField: "testHeader2",
        header: "Prueba 2",
        width: "5%",
        wrapped: false,
      },
    ];
    const { container } = render(
      <Table
        dataset={data}
        exportCsv={false}
        headers={testHeaders}
        id={"testTable"}
        pageSize={25}
        search={false}
      />
    );

    expect(screen.queryByRole("table")).toBeInTheDocument();
    expect(
      screen.queryByText("table.noDataIndication")
    ).not.toBeInTheDocument();
    expect(screen.queryAllByRole("columnheader")).toHaveLength(2);
    expect(container.querySelectorAll("#testTable")).toHaveLength(1);
  });

  it("should render a table", async (): Promise<void> => {
    expect.hasAssertions();

    const handleChange: jest.Mock = jest.fn();
    const handleDelete: jest.Mock = jest.fn();
    const handleOnSelect: jest.Mock = jest.fn(
      (
        row: Readonly<{ uniqueId: number }>,
        _isSelect: boolean,
        rowIndex: number
      ): boolean => {
        return row.uniqueId === rowIndex;
      }
    );
    const testHeaders: IHeaderConfig[] = [
      {
        dataField: "statusHeader",
        formatter: statusFormatter,
        header: "Prueba 1",
        width: "25%",
      },
      {
        dataField: "deleteHeader",
        deleteFunction: handleDelete,
        formatter: deleteFormatter,
        header: "Prueba 2",
        width: "25%",
      },
      {
        changeFunction: handleChange,
        dataField: "changeHeader",
        formatter: changeFormatter,
        header: "Prueba 3",
        width: "25%",
      },
    ];
    const data: Record<string, unknown>[] = [
      {
        changeHeader: "Inactive",
        deleteHeader: "",
        id: "139431",
        statusHeader: "Created",
      },
      {
        changeHeader: "Inactive",
        deleteHeader: "",
        id: "4323491",
        statusHeader: "value",
      },
    ];
    const selectionMode: ISelectRowProps = {
      clickToSelect: false,
      hideSelectColumn: false,
      mode: "checkbox",
      onSelect: handleOnSelect,
      onSelectAll: jest.fn(),
    };
    render(
      <Table
        dataset={data}
        exportCsv={true}
        headers={testHeaders}
        id={"testTable"}
        pageSize={10}
        search={true}
        selectionMode={selectionMode}
      />
    );

    expect(screen.queryByRole("table")).toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "Search this table" })
    ).toBeInTheDocument();
    expect(screen.getAllByRole("columnheader")).toHaveLength(
      testHeaders.length + 1
    );
    expect(
      screen.queryByRole("button", { name: "group.findings.exportCsv.text" })
    ).toBeInTheDocument();

    userEvent.click(within(screen.getAllByRole("row")[1]).getByRole("button"));
    userEvent.click(
      within(
        within(screen.getAllByRole("row")[1]).getByRole("cell", {
          name: "Active",
        })
      ).getByRole("checkbox")
    );
    userEvent.click(screen.getAllByRole("checkbox")[1]);

    await waitFor((): void => {
      expect(handleChange).toHaveBeenCalledTimes(1);
    });

    expect(handleDelete).toHaveBeenCalledTimes(1);
    expect(handleOnSelect.mock.results[0].value).toBe(true);

    jest.clearAllMocks();
  });
});
