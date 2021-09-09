import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";

import { Can } from "utils/authz/Can";
import {
  authzGroupContext,
  authzPermissionsContext,
  groupAttributes,
  userLevelPermissions,
} from "utils/authz/config";
import { Have } from "utils/authz/Have";

describe("Authorization", (): void => {
  it("should return functions", (): void => {
    expect.hasAssertions();

    expect(typeof Can).toStrictEqual("function");
    expect(typeof Have).toStrictEqual("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    userLevelPermissions.update([{ action: "resolve_hacker" }]);
    const wrapper: ReactWrapper = mount(
      <Can do={"resolve_hacker"}>
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

    groupAttributes.update([{ action: "has_asm" }]);

    const wrapper: ReactWrapper = mount(
      <Have I={"has_asm"}>
        <p>{"I have ASM"}</p>
      </Have>,
      {
        wrappingComponent: authzGroupContext.Provider,
        wrappingComponentProps: { value: groupAttributes },
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).toContain("I have ASM");
  });

  it("should not render", (): void => {
    expect.hasAssertions();

    userLevelPermissions.update([]);
    const wrapper: ReactWrapper = mount(
      <Can do={"resolve_hacker"}>
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
      <Have I={"has_asm"}>
        <p>{"I have ASM"}</p>
      </Have>,
      {
        wrappingComponent: authzGroupContext.Provider,
        wrappingComponentProps: { value: groupAttributes },
      }
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.text()).not.toContain("I have ASM");
  });
});
