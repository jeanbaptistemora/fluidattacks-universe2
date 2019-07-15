import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { DataAlignType } from "react-bootstrap-table";
import { IHeader } from "../../../../components/DataTable";
import { default as SimpleTable } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("Simple table", () => {

  it("should return a function", () => {
    expect(typeof (SimpleTable))
      .toEqual("function");
  });

  it("should render table", () => {
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
      <SimpleTable
        id="testTable"
        enableRowSelection={true}
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
});
