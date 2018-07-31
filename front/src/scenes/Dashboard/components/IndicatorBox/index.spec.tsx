import { shallow, configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { expect } from 'chai';
import IndicatorBox from './index';
import 'mocha'
import React from 'react';
import { Col } from "react-bootstrap";
import style from "./index.css";

configure({ adapter: new Adapter() });

describe('Indicator Box', () => {

  it('should return a function', () => {
    expect(typeof(IndicatorBox)).to.equal('function');
  });

  it('should have icon', () => {
    const wrapper = shallow((
      <IndicatorBox 
        backgroundColor="#070"
        color="#700"
        icon="fa fa-star"
        name="Unit test"
        quantity="666"
        title="Unit title"
      />
    ));
    expect(wrapper.contains(<span className="fa fa-star"/>)).to.equal(true);
  });
 
  it('should be render', () => {
    const wrapper = shallow(
      <IndicatorBox 
        backgroundColor="#070"
        color="#700"
        icon="fa fa-star"
        name="Unit test"
        quantity="666"
        title="Unit title"
      />
    );

    expect(
      wrapper.contains(
        <Col xs={12} md={3}>
          <div
            className={style.widgetbox}
            data-toggle="tooltip"
            data-placement="top"
            title="Unit title"
            style={{backgroundColor: "#070", color: "#700"}}
          >
            <Col xs={4} md={4}>
              <div className={style.widgeticon}>
                  <span className="fa fa-star"/>
              </div>
            </Col>
            <Col xs={8} md={8}>
              <div
                data-toggle="counter"
                className={style.widgetvalue}
              >
                666
              </div>
              <div className={style.widgetdesc}>
                Unit test
              </div>
            </Col>
          </div>
        </Col>
      )
    ).to.equal(true);
  });
});
