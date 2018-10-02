import * as React from 'react';
import { expect } from 'chai';
import { shallow, configure } from 'enzyme';
import DataTable from './index';
import { DataAlignType } from 'react-bootstrap-table';
import 'mocha';
import Adapter from 'enzyme-adapter-react-16';

configure({ adapter: new Adapter() });

describe('Data table', () => {

  it('should return a function', () => {
    expect(typeof(DataTable)).to.equal('function');
  });

  it('should render title', () => {
    const data = [
      {
          test_header: "value 1",
          test_header2: "value 2"
      }
    ];
    const testHeaders = [
      {
        align: "center" as DataAlignType,
        isStatus: false,
        width: "5%",
        wrapped: false,
        header: "Prueba 1",
        dataField: "test_header",
        isDate: false
      },
      {
        align: "center" as DataAlignType,
        isStatus: false,
        width: "5%",
        wrapped: false,
        header: "Prueba 2",
        dataField: "test_header2",
        isDate: false
      }
    ];
    const wrapper = shallow(
      <DataTable
        id="testTable"
        enableRowSelection={false}
        dataset={data}
        exportCsv={false}
        search={false}
        headers={testHeaders}
        onClickRow={()=>{}}
        pageSize={25}
        title="Unit test table"
      />
    );
    expect(
      wrapper.contains(
        <h1>
          Unit test table
        </h1>
      )
    ).to.equal(true);
  });

  it('should render table', () => {
    const data = [
      {
          "Test header": "value 1",
          "Test header2": "value 2"
      }
    ];
    const testHeaders = [
      {
        align: "center" as DataAlignType,
        isStatus: false,
        width: "5%",
        wrapped: false,
        header: "Prueba 1",
        dataField: "test_header",
        isDate: false
      },
      {
        align: "center" as DataAlignType,
        isStatus: false,
        width: "5%",
        wrapped: false,
        header: "Prueba 2",
        dataField: "test_header2",
        isDate: false
      }
    ];
    const wrapper = shallow(
      <DataTable
        id="testTable"
        enableRowSelection={false}
        dataset={data}
        exportCsv={false}
        search={false}
        headers={testHeaders}
        onClickRow={()=>{}}
        pageSize={25}
        title="Unit test table"
      />
    );
    let component = wrapper.find(<table/>)
    expect(component).to.exist;
  });
});
