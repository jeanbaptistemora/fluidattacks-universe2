import type { ChartData } from "chart.js";
import { HorizontalBarIndicator } from "scenes/Dashboard/components/HorizontalBarIndicator";
import React from "react";
import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";

describe("HorizontalBarIndicator", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof HorizontalBarIndicator).toStrictEqual("function");
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const DATA_PARAM2: number = 3;
    const data: ChartData = {
      datasets: [{ data: [4, DATA_PARAM2] }],
      labels: ["test", "test2"],
    };
    const wrapper: ShallowWrapper = shallow(
      <HorizontalBarIndicator data={data} name={"Unit header"} options={{}} />
    );

    expect(wrapper).toHaveLength(1);
  });
});
