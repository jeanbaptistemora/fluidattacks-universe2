import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { default as Frame } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Frame", () => {

  it("should return a function", () => {
    expect(typeof (Frame)).to
      .equal("function");
  });

  it("should be render", () => {
    const wrapper: ShallowWrapper = shallow((
      <Frame
        src="https://fluidattacks.com/forms/cierres"
        height={3000}
        id="id"
      />
    ));
    const element: JSX.Element = (
      <Row>
        <Col xs={12} md={12} sm={12}>
          <iframe
            id="id"
            width="100%"
            scrolling="no"
            frameBorder="0"
            height={3000}
            src="https://fluidattacks.com/forms/cierres"
          />
        </Col>
      </Row>);
    expect(wrapper.contains(element)).to
      .equal(true);
  });

});
