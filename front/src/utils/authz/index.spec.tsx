import { Can } from "./Can/index";
import { Have } from "./Have/index";
import React from "react";
import { ReactWrapper, mount } from "enzyme";
import {
  authzGroupContext,
  authzPermissionsContext,
  groupAttributes,
  userLevelPermissions,
} from "./config";

describe("Authorization", (): void => {
  it("should return functions", (): void => {
    expect.hasAssertions();

    expect(typeof Can).toStrictEqual("function");
    expect(typeof Have).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    userLevelPermissions.update([{ action: "resolve_analyst" }]);
    const wrapper: ReactWrapper = mount(
      <Can do={"resolve_analyst"}>
        <p>{"someone@fluidattacks.com"}</p>
      </Can>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: userLevelPermissions },
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toContain("someone@fluidattacks.com");
  });

  it("should render Have", (): void => {
    expect.hasAssertions();

    groupAttributes.update([{ action: "has_integrates" }]);

    const wrapper: ReactWrapper = mount(
      <Have I={"has_integrates"}>
        <p>{"I have Integrates"}</p>
      </Have>,
      {
        wrappingComponent: authzGroupContext.Provider,
        wrappingComponentProps: { value: groupAttributes },
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toContain("I have Integrates");
  });

  it("should not render", (): void => {
    expect.hasAssertions();

    userLevelPermissions.update([]);
    const wrapper: ReactWrapper = mount(
      <Can do={"resolve_analyst"}>
        <p>{"someone@fluidattacks.com"}</p>
      </Can>,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: userLevelPermissions },
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).not.toContain("someone@fluidattacks.com");
  });

  it("should not render Have", (): void => {
    expect.hasAssertions();

    groupAttributes.update([]);

    const wrapper: ReactWrapper = mount(
      <Have I={"has_integrates"}>
        <p>{"I have Integrates"}</p>
      </Have>,
      {
        wrappingComponent: authzGroupContext.Provider,
        wrappingComponentProps: { value: groupAttributes },
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).not.toContain("I have Integrates");
  });
});
