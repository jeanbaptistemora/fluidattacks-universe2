import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';
import DataTable from './index';
import ReactTable from "react-table";
import 'mocha';
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

Enzyme.configure({ adapter: new Adapter() });

describe('Data table', () => {

  it('should return a function', () => {
    expect(typeof(DataTable)).to.equal('function');
  });

  it('should render title', () => {
    const data = [
      {
          "Test header": "value 1",
          "Test header2": "value 2"
      }
    ];
    const wrapper = shallow(
      <DataTable
        dataset={data}
        onClickRow={()=>{}}
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
    const wrapper = shallow(
      <DataTable
        dataset={data}
        onClickRow={()=>{}}
        title="Unit test table"
      />
    );
    let component = wrapper.find(<ReactTable/>)
    expect(component).to.exist;
  });
});
