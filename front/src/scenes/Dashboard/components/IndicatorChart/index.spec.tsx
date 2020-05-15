import { Datum } from "@nivo/line";
import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { IndicatorChart } from "./index";

describe("Indicator Chart", () => {
  const dataChart: Datum[][] = JSON.parse(JSON.stringify([
    [{y: 2, x: "Jun 10 - 16, 2019"}, {y: 12, x: "Jun 17 - 23, 2019"}],
    [{y: 0, x: "Jun 10 - 16, 2019"}, {y: 0, x: "Jun 17 - 23, 2019"}],
    [{y: 0, x: "Jun 10 - 16, 2019"}, {y: 0, x: "Jun 17 - 23, 2019"}],
    [{y: 0, x: "Jun 10 - 16, 2019"}, {y: 0, x: "Jun 17 - 23, 2019"}]]));

  it("should return a function", () => {
    expect(typeof (IndicatorChart))
      .toEqual("function");
  });

  it("should render an indicator chart", () => {

    const wrapper: ShallowWrapper = shallow(
      <IndicatorChart dataChart={dataChart}/>,
    );

    expect(wrapper)
      .toHaveLength(1);
  });
});
