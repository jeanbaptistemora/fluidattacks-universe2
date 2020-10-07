import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { MemoryRouter } from "react-router";
import { ContentTab } from "scenes/Dashboard/components/ContentTab";

describe("ContentTab", () => {

  it("should return a function", (): void => {
    expect(typeof (ContentTab))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter>
        <ContentTab
          icon="test-icon"
          id="test-id"
          link="test-link"
          title="Tab-Title"
          tooltip="Tab-Tooltip"
        />
      </MemoryRouter>,
    );
    expect(wrapper.find("#test-id")
        .hostNodes())
      .toHaveLength(1);
    expect(wrapper.find("#test-id")
        .at(0)
        .text())
      .toContain("Tab-Title");
  });
});
