import { DataTableNext } from "./index";
import { IHeader } from "./types";
import * as React from "react";
import { ReactWrapper, ShallowWrapper, mount, shallow } from "enzyme";
import {
  approveFormatter,
  changeFormatter,
  deleteFormatter,
  statusFormatter,
} from "./formatters";

describe("Data table next", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof DataTableNext).toStrictEqual("function");
  });

  it("should render an empty table", (): void => {
    expect.hasAssertions();
    const selectionMode: SelectRowOptions = {
      clickToSelect: true,
      mode: "checkbox",
    };
    const remote: RemoteProps = {
      cellEdit: false,
      filter: false,
      pagination: false,
      sort: false,
    };
    const data: Record<string, unknown>[] = [];
    const testHeaders: IHeader[] = [];
    const wrapper: ShallowWrapper = shallow(
      <DataTableNext
        bordered={false}
        dataset={data}
        exportCsv={false}
        headers={testHeaders}
        id={"testTable"}
        onClickRow={undefined}
        pageSize={25}
        remote={remote}
        search={false}
        selectionMode={selectionMode}
        title={"Unit test table"}
      />
    );
    expect(wrapper).toHaveLength(1);
  });

  it("should render dynamic headers", (): void => {
    expect.hasAssertions();
    const data: Record<string, unknown>[] = [
      {
        test_header: "value 1",
        test_header2: "value 2",
      },
    ];
    const selectionMode: SelectRowOptions = {
      clickToSelect: true,
      mode: "checkbox",
    };
    const remote: RemoteProps = {
      cellEdit: false,
      filter: false,
      pagination: false,
      sort: false,
    };
    const testHeaders: IHeader[] = [];
    const wrapper: ShallowWrapper = shallow(
      <DataTableNext
        bordered={false}
        dataset={data}
        exportCsv={false}
        headers={testHeaders}
        id={"testTable"}
        onClickRow={undefined}
        pageSize={25}
        remote={remote}
        search={false}
        selectionMode={selectionMode}
        title={"Unit test table"}
      />
    );
    expect(wrapper).toHaveLength(1);
  });

  it("should render a title", (): void => {
    expect.hasAssertions();
    const data: Record<string, unknown>[] = [
      {
        test_header: "Submitted",
        test_header2: "Rejected",
        test_header3: "Inactive",
        test_header4: "Active",
      },
    ];
    const selectionMode: SelectRowOptions = {
      clickToSelect: true,
      mode: "checkbox",
    };
    const remote: RemoteProps = {
      cellEdit: false,
      filter: false,
      pagination: false,
      sort: false,
    };
    const testHeaders: IHeader[] = [
      {
        align: "center",
        dataField: "test_header",
        formatter: statusFormatter,
        header: "Prueba 1",
        width: "5%",
        wrapped: false,
      },
      {
        align: "center",
        dataField: "test_header2",
        formatter: statusFormatter,
        header: "Prueba 2",
        width: "5%",
        wrapped: false,
      },
      {
        align: "center",
        dataField: "test_header3",
        formatter: statusFormatter,
        header: "Prueba 3",
        width: "5%",
        wrapped: false,
      },
      {
        align: "center",
        dataField: "test_header4",
        formatter: statusFormatter,
        header: "Prueba 4",
        width: "5%",
        wrapped: false,
      },
    ];
    const wrapper: ReactWrapper = mount(
      <DataTableNext
        bordered={false}
        dataset={data}
        exportCsv={false}
        headers={testHeaders}
        id={"testTable"}
        onClickRow={undefined}
        pageSize={25}
        remote={remote}
        search={false}
        selectionMode={selectionMode}
        title={"Unit test table"}
      />
    ).find("h3");
    expect(wrapper).toContainEqual(
      <h3 className={"title"}>{"Unit test table"}</h3>
    );
  });

  it("should render a table with id", (): void => {
    expect.hasAssertions();
    const data: Record<string, unknown>[] = [
      {
        test_header: "value 1",
        test_header2: "value 2",
      },
    ];
    const remote: RemoteProps = {
      cellEdit: false,
      filter: false,
      pagination: false,
      sort: false,
    };
    const testHeaders: IHeader[] = [
      {
        align: "center",
        dataField: "test_header",
        header: "Prueba 1",
        width: "5%",
        wrapped: false,
      },
      {
        align: "center",
        dataField: "test_header2",
        header: "Prueba 2",
        width: "5%",
        wrapped: false,
      },
    ];
    const wrapper: ShallowWrapper = shallow(
      <DataTableNext
        bordered={false}
        dataset={data}
        exportCsv={false}
        headers={testHeaders}
        id={"testTable"}
        onClickRow={undefined}
        pageSize={25}
        remote={remote}
        search={false}
        title={"Unit test table"}
      />
    );
    expect(wrapper.find("#testTable")).toHaveLength(1);
  });

  it("should render a table", (): void => {
    expect.hasAssertions();
    const handleApprove: jest.Mock = jest.fn();
    const handleChange: jest.Mock = jest.fn();
    const handleDelete: jest.Mock = jest.fn();
    const testHeaders: IHeader[] = [
      {
        align: "center",
        dataField: "statusHeader",
        formatter: statusFormatter,
        header: "Prueba 1",
        width: "25%",
      },
      {
        align: "center",
        approveFunction: handleApprove,
        dataField: "approveHeader",
        formatter: approveFormatter,
        header: "Prueba 2",
        width: "25%",
      },
      {
        align: "center",
        dataField: "deleteHeader",
        deleteFunction: handleDelete,
        formatter: deleteFormatter,
        header: "Prueba 3",
        width: "25%",
      },
      {
        align: "center",
        changeFunction: handleChange,
        dataField: "changeHeader",
        formatter: changeFormatter,
        header: "Prueba 4",
        width: "25%",
      },
    ];
    const data: Record<string, unknown>[] = [
      {
        approveHeader: "",
        changeHeader: "Inactive",
        deleteHeader: "",
        statusHeader: "Created",
      },
      {
        approveHeader: "",
        changeHeader: "Inactive",
        deleteHeader: "",
        statusHeader: "value",
      },
    ];
    const selectionMode: SelectRowOptions = {
      clickToSelect: true,
      mode: "checkbox",
    };
    const remote: RemoteProps = {
      cellEdit: false,
      filter: false,
      pagination: false,
      sort: false,
    };
    const wrapper: ReactWrapper = mount(
      <DataTableNext
        bordered={false}
        dataset={data}
        exportCsv={true}
        headers={testHeaders}
        id={"testTable"}
        onTableChange={jest.fn()}
        pageSize={1}
        remote={remote}
        search={true}
        selectionMode={selectionMode}
        tableBody={undefined}
        tableHeader={undefined}
        title={"Unit test table"}
      />
    );

    const proceedApproveFunction: ReactWrapper = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell")
      .at(1)
      .find("a");
    proceedApproveFunction.simulate("click");
    const position: number = 3;
    const proceedChangeFunction: ReactWrapper = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell")
      .at(position)
      .find("div")
      .at(0);
    proceedChangeFunction.simulate("click");
    const proceedDeleteFunction: ReactWrapper = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell")
      .at(2)
      .find("a");
    proceedDeleteFunction.simulate("click");

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find("BootstrapTable").find("HeaderCell")).toHaveLength(
      testHeaders.length
    );
    expect(wrapper.find("ExportCSVButton")).toHaveLength(1);
    expect(wrapper.find("SearchBar")).toHaveLength(1);
    expect(wrapper.find("DropdownButton")).toHaveLength(1);
    expect(handleApprove.mock.calls).toHaveLength(1);
    expect(handleChange.mock.calls).toHaveLength(1);
    expect(handleDelete.mock.calls).toHaveLength(1);
  });
});
