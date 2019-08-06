import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { DataAlignType } from "react-bootstrap-table";
import { dataTable as DataTable, dateFormatter, IHeader } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Data table", () => {

  it("should return a function", () => {
    expect(typeof (DataTable))
      .toEqual("function");
  });

  it("should render an empty table", () => {
    const data: object[] = [];
    const testHeaders: IHeader[] = [];
    const wrapper: ShallowWrapper = shallow(
      <DataTable
        id="testTable"
        enableRowSelection={false}
        dataset={data}
        exportCsv={false}
        search={false}
        headers={testHeaders}
        onClickRow={undefined}
        pageSize={25}
        title="Unit test table"
        selectionMode="none"
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a table without data", () => {
    const data: object[] = [];
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
        selectionMode="none"
      />,
    );
    expect(wrapper.find("TableHeaderColumn"))
      .toHaveLength(2);
  });

  it("should render a table without header", () => {
    const data: object[] = [
      {
        test_header: "value 1",
        test_header2: "value 2",
      },
    ];
    const testHeaders: IHeader[] = [];
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
        selectionMode="none"
      />,
    );
    expect(wrapper.find("TableHeaderColumn"))
      .toHaveLength(3);
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
        selectionMode="none"
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
        selectionMode="none"
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
        selectionMode="none"
      />,
    );

    expect(wrapper)
      .toHaveLength(1);
  });

  it("should return date", () => {
    const formatter: string = dateFormatter("25-05-19");
    expect(dateFormatter(formatter))
      .toEqual("25-05-19");
  });

  it("should return date without time", () => {
    const formatter: string = dateFormatter("25-05-19 12:00:00");
    expect(dateFormatter(formatter))
      .toEqual("25-05-19");
  });

});
