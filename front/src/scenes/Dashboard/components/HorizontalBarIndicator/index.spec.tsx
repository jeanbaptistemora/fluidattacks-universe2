import { ChartData } from "chart.js";
import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { HorizontalBarIndicator } from "./index";

describe("HorizontalBarIndicator", () => {

  it("should return a function", () => {
    expect(typeof (HorizontalBarIndicator))
      .toEqual("function");
  });

  it("should render a component", () => {
    const data: ChartData = {
      datasets: [ { data: [4, 3] } ],
      labels: ["test", "test2"],
    };
    const wrapper: ShallowWrapper = shallow(
      <HorizontalBarIndicator
        data={data}
        name="Unit header"
        options={{}}
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

});
