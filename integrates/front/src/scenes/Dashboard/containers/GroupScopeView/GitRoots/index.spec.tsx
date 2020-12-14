import { GitModal } from "./gitModal";
import { GitRoots } from ".";
import { MockedProvider } from "@apollo/react-testing";
import { Provider } from "react-redux";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { SwitchButton } from "components/SwitchButton";
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

    const refetch: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider>
          <GitRoots groupName={"unittesting"} onUpdate={refetch} roots={[]} />
        </MockedProvider>
      </Provider>
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find("table")).toHaveLength(1);
  });

  it("should render action buttons", (): void => {
    expect.hasAssertions();

    const refetch: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider>
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "backend_api_mutations_add_git_root_mutate" },
                { action: "backend_api_mutations_update_git_root_mutate" },
              ])
            }
          >
            <GitRoots groupName={"unittesting"} onUpdate={refetch} roots={[]} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );

    expect(wrapper).toHaveLength(1);

    act((): void => {
      wrapper.update();
    });

    const addButton: ReactWrapper = wrapper.find("button").at(0);

    expect(addButton).toHaveLength(1);

    const editButton: ReactWrapper = wrapper.find("button").at(1);

    expect(editButton).toHaveLength(1);
    expect(editButton.prop("disabled")).toStrictEqual(true);

    expect(wrapper.find(GitModal)).toHaveLength(0);

    addButton.simulate("click");

    expect(wrapper.find(GitModal)).toHaveLength(1);
  });

  it("should render modal", (): void => {
    expect.hasAssertions();

    const handleClose: jest.Mock = jest.fn();
    const handleSubmit: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <authzPermissionsContext.Provider
          value={new PureAbility([{ action: "update_git_root_filter" }])}
        >
          <MockedProvider>
            <GitModal
              initialValues={undefined}
              onClose={handleClose}
              onSubmit={handleSubmit}
            />
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </Provider>
    );

    expect(wrapper).toHaveLength(1);

    // Repository fields
    expect(wrapper.find({ name: "url" }).find("input")).toHaveLength(1);
    expect(wrapper.find({ name: "branch" }).find("input")).toHaveLength(1);
    expect(wrapper.find({ name: "environment" }).find("input")).toHaveLength(1);

    // Health Check
    expect(wrapper.find({ name: "includesHealthCheck" })).toHaveLength(0);

    wrapper.find(SwitchButton).at(0).simulate("click");
    wrapper.find(SwitchButton).at(1).simulate("click");

    expect(
      wrapper.find({ name: "includesHealthCheck" }).find("input")
    ).toHaveLength(1);

    // Filters
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
