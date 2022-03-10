import type { ReactWrapper, ShallowWrapper } from "enzyme";
import { mount, shallow } from "enzyme";
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
    const wrapper: ShallowWrapper = shallow(
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

    expect(wrapper).toHaveLength(1);
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
    const wrapper: ShallowWrapper = shallow(
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

    expect(wrapper).toHaveLength(1);
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
    const wrapper: ShallowWrapper = shallow(
      <Table
        dataset={data}
        exportCsv={false}
        headers={testHeaders}
        id={"testTable"}
        pageSize={25}
        search={false}
      />
    );

    expect(wrapper.find("#testTable")).toHaveLength(1);
  });

  it("should render a table", (): void => {
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
    const wrapper: ReactWrapper = mount(
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

    const proceedChangeFunction: ReactWrapper = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell")
      .at(2)
      .find("div")
      .at(0);
    proceedChangeFunction.simulate("click");
    const proceedDeleteFunction: ReactWrapper = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell")
      .at(1)
      .find("button");
    proceedDeleteFunction.simulate("click");
    const checkboxInput: ReactWrapper = wrapper.find("SelectionCell").at(0);
    checkboxInput.simulate("click");

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find("BootstrapTable").find("HeaderCell")).toHaveLength(
      testHeaders.length
    );
    expect(wrapper.find("ExportCSVButtonWrapper")).toHaveLength(1);
    expect(wrapper.find("SearchBar")).toHaveLength(1);
    expect(handleChange.mock.calls).toHaveLength(1);
    expect(handleDelete.mock.calls).toHaveLength(1);
    expect(handleOnSelect.mock.results[0].value).toBe(true);
  });
});
