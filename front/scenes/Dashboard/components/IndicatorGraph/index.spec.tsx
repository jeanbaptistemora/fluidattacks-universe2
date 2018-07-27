import React from 'react';
import { expect } from 'chai';
import { shallow } from 'enzyme';
import IndicatorGraph from './index';
import 'mocha'
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import style from "./index.css";

Enzyme.configure({ adapter: new Adapter() });

describe('Indicator Graph', () => {

  it('should return a function', () => {
    expect(typeof(IndicatorGraph)).to.equal('function');
  });

  it('should have header', () => {
    const data = {
      labels: [
        "Open",
        "Close",
      ],
      datasets: [{
        backgroundColor: ["#ff1a1a", "#31c0be"],
        data: [6, 4],
        hoverBackgroundColor: ["#e51414", "#258c8a"],
      }],
    };
    const wrapper = shallow((
      <IndicatorGraph
        data={data}
        name="Unit header"
      />
    ));
    expect(wrapper.contains(<h3>Unit header</h3>)).to.equal(true);
  });

});
