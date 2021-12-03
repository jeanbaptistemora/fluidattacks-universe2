import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";

import { TrackingItem } from "scenes/Dashboard/components/TrackingItem";

describe("TrackingItem", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof TrackingItem).toStrictEqual("function");
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <TrackingItem
        accepted={1}
        acceptedUndefined={0}
        assigned={"testmanager@test.test"}
        closed={0}
        cycle={1}
        date={"2019-01-17"}
        justification={"test justification temporarily accepted"}
        open={1}
      />
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toContain("2019-01-17");
    expect(wrapper.text()).toContain("Cycle: 1,");
    expect(wrapper.text()).toContain("Vulnerabilities found:\u00a01");
    expect(wrapper.text()).toContain(
      "Justification:\u00a0test justification temporarily accepted"
    );
  });

  it("should render root item", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <TrackingItem
        accepted={0}
        acceptedUndefined={0}
        closed={0}
        cycle={0}
        date={"2019-01-17"}
        open={1}
      />
    );

    expect(wrapper.text()).toContain("2019-01-17");
    expect(wrapper.text()).toContain("Found");
    expect(wrapper.text()).toContain("Vulnerabilities found:\u00a01");
  });

  it("should render closed item", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <TrackingItem
        accepted={0}
        acceptedUndefined={0}
        closed={1}
        cycle={2}
        date={"2019-01-17"}
        open={0}
      />
    );

    expect(wrapper.find("li").prop("className")).toContain("green");
  });
});
