import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { IndicatorGraph } from "./index";

describe("Indicator Graph", () => {

  it("should return a function", () => {
    expect(typeof (IndicatorGraph))
      .toEqual("function");
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
    const wrapper: ShallowWrapper = shallow(
      <IndicatorGraph
        data={data}
        name="Unit header"
      />,
    );
    expect(wrapper.contains(<h3>Unit header</h3>))
      .toBeTruthy();
  });

});
