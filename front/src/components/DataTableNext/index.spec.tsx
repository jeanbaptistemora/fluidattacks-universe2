import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
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

  it("should render a title", () => {
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
        "Test header": "value 1",
        "Test header2": "value 2",
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
        selectionMode={selectionMode}
      />,
    );
    expect(wrapper.find("#testTable"))
      .toHaveLength(1);
  });

  it("should render a table", () => {
    const data: object[] = [
      {
        "Test header": "value 1",
        "Test header2": "value 2",
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
        selectionMode={selectionMode}
      />,
    );

    expect(wrapper)
      .toHaveLength(1);
  });
});
