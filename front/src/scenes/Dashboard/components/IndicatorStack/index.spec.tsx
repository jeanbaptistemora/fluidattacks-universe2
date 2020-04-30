import { ChartData } from "chart.js";
import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { IndicatorStack } from "./index";

describe("IndicatorStack", () => {

  it("should return a function", () => {
    expect(typeof (IndicatorStack))
      .toEqual("function");
  });

  it("should render a component", () => {
    const data: ChartData = {
      datasets: [
        { data: [4, 3], stack: "2" },
        { data: [2, 4], stack: "2" },
      ],
      labels: ["test", "test2"],
    };
    const wrapper: ShallowWrapper = shallow(
      <IndicatorStack
        data={data}
        name="Unit header"
        height={100}
        options={{legend: { display: true, position: "top" }}}
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });

});
