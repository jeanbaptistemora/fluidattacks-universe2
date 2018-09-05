import { shallow, configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import { expect } from "chai";
import FieldBox from "./index";
import { Col } from "react-bootstrap";
import "mocha";
import React from "react";

configure({ adapter: new Adapter() });

describe('Field Box', () => {

  it('should return a function', () => {
    expect(typeof(FieldBox)).to.equal('function');
  });

  it('should be render', () => {
    const wrapper = shallow(
      <FieldBox
        title="Unit test"
        content="Unit test description"
      />
    );

    expect(
      wrapper.contains(
        <div className="row table-row">
          <Col xs={12} md={4}>
            <div className="table-head">
              <label><b>Unit test</b></label>
            </div>
          </Col>
          <Col xs={12} md={8}>
            <p>
              Unit test description
            </p>
          </Col>
        </div>
      )
    ).to.equal(true);
  });
});
