import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { ContentTab } from "./index";

describe("ContentTab", () => {

  it("should return a function", (): void => {
    expect(typeof (ContentTab))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <ContentTab
        icon="test-icon"
        id="test-id"
        link="test-link"
        title="Tab-Title"
        tooltip="Tab-Tooltip"
      />,
    );
    expect(wrapper.find("#test-id")
        .hostNodes())
      .toHaveLength(1);
    expect(wrapper.find("#test-id")
        .text())
      .toContain("Tab-Title");
  });
});
