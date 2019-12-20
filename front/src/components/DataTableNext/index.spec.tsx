import { configure, mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { approveFormatter, changeFormatter, deleteFormatter, statusFormatter } from "./formatters";
import { DataTableNext } from "./index";
import { IHeader } from "./types";

configure({ adapter: new ReactSixteenAdapter() });
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

describe("Data table next", () => {

  it("should return a function", () => {
    expect(typeof (DataTableNext))
      .toEqual("function");
  });

  it("should render an empty table", () => {
    const data: object[] = [];
    const testHeaders: IHeader[] = [];
    const wrapper: ShallowWrapper = shallow(
      <DataTableNext
        id="testTable"
        bordered={false}
        dataset={data}
        exportCsv={false}
        remote={remote}
        search={false}
        headers={testHeaders}
        onClickRow={undefined}
        pageSize={25}
        title="Unit test table"
        selectionMode={selectionMode}
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render dynamic headers", () => {
    const data: object[] = [
      {
        test_header: "value 1",
        test_header2: "value 2",
      },
    ];
    const testHeaders: IHeader[] = [];
    const wrapper: ShallowWrapper = shallow(
      <DataTableNext
        id="testTable"
        bordered={false}
        dataset={data}
        exportCsv={false}
        remote={remote}
        search={false}
        headers={testHeaders}
        onClickRow={undefined}
        pageSize={25}
        title="Unit test table"
        selectionMode={selectionMode}
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a title", () => {
    const data: object[] = [
      {
        test_header: "Submitted",
        test_header2: "Rejected",
        test_header3: "Inactive",
        test_header4: "Active",
      },
    ];
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
        id="testTable"
        bordered={false}
        dataset={data}
        exportCsv={false}
        remote={remote}
        search={false}
        headers={testHeaders}
        onClickRow={undefined}
        pageSize={25}
        title="Unit test table"
        selectionMode={selectionMode}
      />,
    )
      .find("h3");
    expect(wrapper)
      .toContainEqual(
        <h3 className="title">
            Unit test table
        </h3>,
      );
  });

  it("should render a table with id", () => {
    const data: object[] = [
      {
        test_header: "value 1",
        test_header2: "value 2",
      },
    ];
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
        id="testTable"
        bordered={false}
        dataset={data}
        exportCsv={false}
        remote={remote}
        search={false}
        headers={testHeaders}
        onClickRow={undefined}
        pageSize={25}
        title="Unit test table"
      />,
    );
    expect(wrapper.find("#testTable"))
      .toHaveLength(1);
  });

  it("should render a table", () => {
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
    const data: object[] = [
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

    const wrapper: ReactWrapper = mount(
      <DataTableNext
        id="testTable"
        bordered={false}
        dataset={data}
        exportCsv={true}
        remote={remote}
        search={true}
        headers={testHeaders}
        onTableChange={jest.fn()}
        pageSize={1}
        title="Unit test table"
        tableBody={undefined}
        tableHeader={undefined}
        selectionMode={selectionMode}
      />,
    );

    const proceedApproveFunction: ReactWrapper = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell")
      .at(1)
      .find("a");
    proceedApproveFunction.simulate("click");
    const proceedChangeFunction: ReactWrapper = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell")
      .at(3)
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

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.find("BootstrapTable")
                  .find("HeaderCell"))
      .toHaveLength(testHeaders.length);
    expect(wrapper.find("ExportCSVButton"))
      .toHaveLength(1);
    expect(wrapper.find("SearchBar"))
      .toHaveLength(1);
    expect(wrapper.find("DropdownButton"))
      .toHaveLength(1);
    expect(handleApprove.mock.calls.length)
      .toEqual(1);
    expect(handleChange.mock.calls.length)
      .toEqual(1);
    expect(handleDelete.mock.calls.length)
      .toEqual(1);
  });
});
