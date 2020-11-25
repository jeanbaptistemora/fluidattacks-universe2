import { GitRoots } from ".";
import { Provider } from "react-redux";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { act } from "react-dom/test-utils";
import { authzPermissionsContext } from "utils/authz/config";
import { mount } from "enzyme";
import store from "store";

describe("GitRoots", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GitRoots).toStrictEqual("function");
  });

  it("should render table", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(<GitRoots roots={[]} />);

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find("table")).toHaveLength(1);
  });

  it("should render action buttons", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <authzPermissionsContext.Provider
        value={
          new PureAbility([
            { action: "backend_api_mutations_add_git_root_mutate" },
          ])
        }
      >
        <GitRoots roots={[]} />
      </authzPermissionsContext.Provider>
    );

    expect(wrapper).toHaveLength(1);

    act((): void => {
      wrapper.update();
    });

    expect(wrapper.text()).toContain("add");
  });

  // Giving TDD a try, will enable next MR
  // eslint-disable-next-line jest/no-disabled-tests
  it.skip("should render modal", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <div />
      </Provider>
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find({ name: "url" }).find("input")).toHaveLength(1);
    expect(wrapper.find({ name: "branch" }).find("input")).toHaveLength(1);
    expect(wrapper.find({ name: "environment" }).find("input")).toHaveLength(1);

    const policyDropdown: ReactWrapper = wrapper
      .find({ name: "policy" })
      .find("select");

    expect(policyDropdown).toHaveLength(1);

    expect(wrapper.find({ name: "paths" })).toHaveLength(0);

    policyDropdown.simulate("change", {
      target: { value: "INCLUDE" },
    });

    expect(wrapper.find({ name: "paths" }).find("input")).toHaveLength(1);

    policyDropdown.simulate("change", {
      target: { value: "EXCLUDE" },
    });

    expect(wrapper.find({ name: "paths" }).find("input")).toHaveLength(1);

    policyDropdown.simulate("change", {
      target: { value: "NONE" },
    });

    expect(wrapper.find({ name: "paths" })).toHaveLength(0);
  });
});
