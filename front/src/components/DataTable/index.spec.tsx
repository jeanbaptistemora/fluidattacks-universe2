import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import * as React from "react";
import { DataAlignType } from "react-bootstrap-table";
import { dataTable as DataTable, IHeader } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Data table", () => {

  it("should return a function", () => {
    expect(typeof (DataTable)).to
      .equal("function");
  });

  it("should render title", () => {
    const data: object = [
      {
        test_header: "value 1",
        test_header2: "value 2",
      },
    ];
    const testHeaders: IHeader[] = [
      {
        align: "center" as DataAlignType,
        dataField: "test_header",
        header: "Prueba 1",
        isDate: false,
        isStatus: false,
        width: "5%",
        wrapped: false,
      },
      {
        align: "center" as DataAlignType,
        dataField: "test_header2",
        header: "Prueba 2",
        isDate: false,
        isStatus: false,
        width: "5%",
        wrapped: false,
      },
    ];
    const wrapper: ShallowWrapper = shallow(
      <DataTable
        id="testTable"
        enableRowSelection={false}
        dataset={data}
        exportCsv={false}
        search={false}
        headers={testHeaders}
        onClickRow={functionMock}
        pageSize={25}
        title="Unit test table"
      />,
    );
    expect(
      wrapper.contains(
        <h1>
          Unit test table
        </h1>,
      ),
    ).to
      .equal(true);
  });

  it("should render table", () => {
    const data: object = [
      {
        "Test header": "value 1",
        "Test header2": "value 2",
      },
    ];
    const testHeaders: IHeader[] = [
      {
        align: "center" as DataAlignType,
        dataField: "test_header",
        header: "Prueba 1",
        isDate: false,
        isStatus: false,
        width: "5%",
        wrapped: false,
      },
      {
        align: "center" as DataAlignType,
        dataField: "test_header2",
        header: "Prueba 2",
        isDate: false,
        isStatus: false,
        width: "5%",
        wrapped: false,
      },
    ];
    const wrapper: ShallowWrapper = shallow(
      <DataTable
        id="testTable"
        enableRowSelection={false}
        dataset={data}
        exportCsv={false}
        search={false}
        headers={testHeaders}
        onClickRow={functionMock}
        pageSize={25}
        title="Unit test table"
      />,
    );
    const component: ShallowWrapper = wrapper.find(<table />);
    expect(component).to.have
      .length(1);
  });
});
