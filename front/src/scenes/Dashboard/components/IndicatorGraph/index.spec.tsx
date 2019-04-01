import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import React from "react";
import { IndicatorGraph } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Indicator Graph", () => {

  it("should return a function", () => {
    expect(typeof (IndicatorGraph)).to
      .equal("function");
  });

  it("should have header", () => {
    const data: object = {
      datasets: [{
        backgroundColor: ["#ff1a1a", "#31c0be"],
        data: [6, 4],
        hoverBackgroundColor: ["#e51414", "#258c8a"],
      }],
      labels: [
        "Close",
        "Open",
      ],
    };
    const wrapper: ShallowWrapper = shallow((
      <IndicatorGraph
        data={data}
        name="Unit header"
      />
    ));
    expect(wrapper.contains(<h3>Unit header</h3>)).to
      .equal(true);
  });

});
