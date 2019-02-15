import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import React from "react";
import { Col } from "react-bootstrap";
import { default as IndicatorBox } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Indicator Box", () => {

  it("should return a function", () => {
    expect(typeof (IndicatorBox)).to
      .equal("function");
  });

  const wrapper: ShallowWrapper = shallow((
    <IndicatorBox
      backgroundColor="#070"
      color="#700"
      icon="fa fa-star"
      name="Unit test"
      quantity="666"
      title="Unit title"
    />
  ));

  it("should have icon", () => {
    expect(wrapper.contains(<span className="fa fa-star" />)).to
      .equal(true);
  });

  it("should render", () => {
    expect(
      wrapper.contains([
        (
          <Col xs={4} md={4}>
            <div>
              <span className="fa fa-star" />
            </div>
          </Col>),
        (
          <Col xs={8} md={8}>
            <div data-toggle="counter">
              666
            </div>
            <div>
              Unit test
            </div>
          </Col>),
      ]),
    ).to
      .equal(true);
  });

  it("should render specified colors", () => {
    expect(JSON.stringify(wrapper.find('[title="Unit title"]')
      .prop<React.CSSProperties>("style"))).to
      .equal(JSON.stringify({ backgroundColor: "#070", color: "#700" }));
  });
});
