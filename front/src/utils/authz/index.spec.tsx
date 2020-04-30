import { mount, ReactWrapper } from "enzyme";
import _ from "lodash";
import React from "react";
import { Can } from "./Can/index";
import { authzContext, userLevelPermissions } from "./config";

describe("Authorization", () => {

  it("should return a function", () => {
    expect(typeof (Can))
      .toEqual("function");
  });

  it("should render", () => {
    userLevelPermissions.update([{ action: "resolve_analyst" }]);
    const wrapper: ReactWrapper = mount(
      <Can do="resolve_analyst">
        <p>someone@fluidattacks.com</p>
      </Can>,
      {
        wrappingComponent: authzContext.Provider,
        wrappingComponentProps: { value: userLevelPermissions },
      },
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("someone@fluidattacks.com");
  });

  it("should not render", () => {
    userLevelPermissions.update([]);
    const wrapper: ReactWrapper = mount(
      <Can do="resolve_analyst">
        <p>someone@fluidattacks.com</p>
      </Can>,
      {
        wrappingComponent: authzContext.Provider,
        wrappingComponentProps: { value: userLevelPermissions },
      },
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .not
      .toContain("someone@fluidattacks.com");
  });
});
