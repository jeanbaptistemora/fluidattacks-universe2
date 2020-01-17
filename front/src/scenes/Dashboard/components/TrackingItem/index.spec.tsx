import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { TrackingItem } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("TrackingItem", () => {

  it("should return a function", (): void => {
    expect(typeof (TrackingItem))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <TrackingItem
        closed={0}
        cycle={1}
        date="2019-01-17"
        effectiveness={0}
        open={1}
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("2019-01-17");
    expect(wrapper.text())
      .toContain("Cycle: 1,\u00a0Open: 1,\u00a0Closed: 0, Effectiveness: 0%");
  });

  it("should render root item", async () => {
    const wrapper: ShallowWrapper = shallow(
      <TrackingItem
        closed={0}
        cycle={0}
        date="2019-01-17"
        effectiveness={0}
        open={1}
      />,
    );
    expect(wrapper.text())
      .toContain("Found,\u00a0Open: 1,\u00a0Closed: 0");
  });

  it("should render closed item", async () => {
    const wrapper: ShallowWrapper = shallow(
      <TrackingItem
        closed={1}
        cycle={2}
        date="2019-01-17"
        effectiveness={100}
        open={0}
      />,
    );
    expect(wrapper.find("li")
      .prop("className"))
      .toContain("green");
  });
});
