import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Col } from "react-bootstrap";
import { default as FieldBox } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Field Box", () => {

  it("should return a function", () => {
    expect(typeof (FieldBox)).to
      .equal("function");
  });

  it("should be render", () => {
    const wrapper: ShallowWrapper = shallow(
      <FieldBox
        title="Unit test"
        content="Unit test description"
      />,
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
        </div>,
      ),
    ).to
      .equal(true);
  });
});
