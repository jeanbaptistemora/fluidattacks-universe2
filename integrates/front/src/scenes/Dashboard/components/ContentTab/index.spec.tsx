import { ContentTab } from "scenes/Dashboard/components/ContentTab";
import { MemoryRouter } from "react-router";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";

describe("ContentTab", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ContentTab).toStrictEqual("function");
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter>
        <ContentTab
          icon={"test-icon"}
          id={"test-id"}
          link={"test-link"}
          title={"Tab-Title"}
          tooltip={"Tab-Tooltip"}
        />
      </MemoryRouter>
    );

    expect(wrapper.find("#test-id").hostNodes()).toHaveLength(1);
    expect(wrapper.find("#test-id").at(0).text()).toContain("Tab-Title");
  });
});
