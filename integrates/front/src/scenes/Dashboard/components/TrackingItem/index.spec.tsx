import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { TrackingItem } from "scenes/Dashboard/components/TrackingItem";

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
        new={0}
        inProgress={1}
        accepted={0}
        acceptedUndefined={0}
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("2019-01-17");
    expect(wrapper.text())
      .toContain("Cycle: 1,");
    expect(wrapper.text())
      .toContain("Status:");
    expect(wrapper.text())
      .toContain("Open: 1,\u00a0Closed: 0, Effectiveness: 0%");
    expect(wrapper.text())
      .toContain("Treatment:");
    expect(wrapper.text())
      .toContain("New: 0,\u00a0In progress: 1,\u00a0Temporally accepted: 0,\u00a0Eternally accepted: 0");
  });

  it("should render root item", async () => {
    const wrapper: ShallowWrapper = shallow(
      <TrackingItem
        closed={0}
        cycle={0}
        date="2019-01-17"
        effectiveness={0}
        open={1}
        new={1}
        inProgress={0}
        accepted={0}
        acceptedUndefined={0}
      />,
    );
    expect(wrapper.text())
      .toContain("2019-01-17");
    expect(wrapper.text())
      .toContain("Found");
    expect(wrapper.text())
      .toContain("Status:");
    expect(wrapper.text())
      .toContain("Open: 1,\u00a0Closed: 0");
  });

  it("should render closed item", async () => {
    const wrapper: ShallowWrapper = shallow(
      <TrackingItem
        closed={1}
        cycle={2}
        date="2019-01-17"
        effectiveness={100}
        open={0}
        new={0}
        inProgress={0}
        accepted={0}
        acceptedUndefined={0}
      />,
    );
    expect(wrapper.find("li")
      .prop("className"))
      .toContain("green");
  });
});
