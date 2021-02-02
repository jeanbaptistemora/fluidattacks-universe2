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
        open={1}
        accepted={1}
        acceptedUndefined={0}
        manager={"testmanager@test.test"}
        justification={"test justification temporally accepted"}
      />,
    );
    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("2019-01-17");
    expect(wrapper.text())
      .toContain("Cycle: 1,");
    expect(wrapper.text())
      .toContain("Vulnerabilities found:\u00a01");
    expect(wrapper.text())
      .toContain("Justification:\u00a0test justification temporally accepted");
  });

  it("should render root item", async () => {
    const wrapper: ShallowWrapper = shallow(
      <TrackingItem
        closed={0}
        cycle={0}
        date="2019-01-17"
        open={1}
        accepted={0}
        acceptedUndefined={0}
      />,
    );
    expect(wrapper.text())
      .toContain("2019-01-17");
    expect(wrapper.text())
      .toContain("Found");
    expect(wrapper.text())
      .toContain("Vulnerabilities found:\u00a01");
  });

  it("should render closed item", async () => {
    const wrapper: ShallowWrapper = shallow(
      <TrackingItem
        closed={1}
        cycle={2}
        date="2019-01-17"
        open={0}
        accepted={0}
        acceptedUndefined={0}
      />,
    );
    expect(wrapper.find("li")
      .prop("className"))
      .toContain("green");
  });
});
