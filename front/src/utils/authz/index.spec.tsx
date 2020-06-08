import { mount, ReactWrapper } from "enzyme";
import _ from "lodash";
import React from "react";
import { Can } from "./Can/index";
import {
  authzGroupContext,
  authzPermissionsContext,
  groupAttributes,
  userLevelPermissions,
} from "./config";
import { Have } from "./Have/index";

describe("Authorization", () => {

  it("should return functions", () => {
    expect(typeof (Can))
      .toEqual("function");
    expect(typeof (Have))
      .toEqual("function");
  });

  it("should render", () => {
    userLevelPermissions.update([{ action: "resolve_analyst" }]);
    const wrapper: ReactWrapper = mount(
      <Can do="resolve_analyst">
        <p>someone@fluidattacks.com</p>
      </Can>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: userLevelPermissions },
      },
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("someone@fluidattacks.com");
  });

  it("should render Have", () => {
    groupAttributes.update([{ action: "has_integrates" }]);

    const wrapper: ReactWrapper = mount(
      <Have I="has_integrates">
        <p>I have Integrates</p>
      </Have>,
      {
        wrappingComponent: authzGroupContext.Provider,
        wrappingComponentProps: { value: groupAttributes },
      },
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .toContain("I have Integrates");
  });

  it("should not render", () => {
    userLevelPermissions.update([]);
    const wrapper: ReactWrapper = mount(
      <Can do="resolve_analyst">
        <p>someone@fluidattacks.com</p>
      </Can>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: userLevelPermissions },
      },
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .not
      .toContain("someone@fluidattacks.com");
  });

  it("should not render Have", () => {
    groupAttributes.update([]);

    const wrapper: ReactWrapper = mount(
      <Have I="has_integrates">
        <p>I have Integrates</p>
      </Have>,
      {
        wrappingComponent: authzGroupContext.Provider,
        wrappingComponentProps: { value: groupAttributes },
      },
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper.text())
      .not
      .toContain("I have Integrates");
  });
});
