import { GitRoots } from ".";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { act } from "react-dom/test-utils";
import { authzPermissionsContext } from "utils/authz/config";
import { mount } from "enzyme";

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
});
