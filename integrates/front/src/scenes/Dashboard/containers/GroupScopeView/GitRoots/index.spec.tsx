import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { MemoryRouter } from "react-router-dom";
import wait from "waait";

import { ManagementModal } from "./ManagementModal";

import { GitRoots } from ".";
import type { IGitRootAttr } from "../types";
import { Button } from "components/Button";
import { SwitchButton } from "components/SwitchButton";
import { ButtonToolbar } from "styles/styledComponents";
import { authzPermissionsContext } from "utils/authz/config";

describe("GitRoots", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GitRoots).toStrictEqual("function");
  });

  it("should render tables", (): void => {
    expect.hasAssertions();

    const refetch: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <MockedProvider>
        <MemoryRouter initialEntries={["/TEST"]}>
          <GitRoots groupName={"unittesting"} onUpdate={refetch} roots={[]} />
        </MemoryRouter>
      </MockedProvider>
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find("table")).toHaveLength(2);
  });

  it("should render action buttons", (): void => {
    expect.hasAssertions();

    const refetch: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <MockedProvider>
        <MemoryRouter initialEntries={["/TEST"]}>
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "api_mutations_add_git_root_mutate" },
                { action: "api_mutations_update_git_root_mutate" },
              ])
            }
          >
            <GitRoots groupName={"unittesting"} onUpdate={refetch} roots={[]} />
          </authzPermissionsContext.Provider>
        </MemoryRouter>
      </MockedProvider>
    );

    expect(wrapper).toHaveLength(1);

    act((): void => {
      wrapper.update();
    });

    const addButton: ReactWrapper = wrapper.find({ id: "git-root-add" }).at(0);

    expect(addButton).toHaveLength(1);
    expect(wrapper.find(ManagementModal)).toHaveLength(0);

    addButton.simulate("click");

    expect(wrapper.find(ManagementModal)).toHaveLength(1);
  });

  it("should render git modal", (): void => {
    expect.hasAssertions();

    const handleClose: jest.Mock = jest.fn();
    const handleSubmit: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <authzPermissionsContext.Provider
        value={new PureAbility([{ action: "update_git_root_filter" }])}
      >
        <ManagementModal
          initialValues={undefined}
          nicknames={[]}
          onClose={handleClose}
          onSubmitEnvs={handleSubmit}
          onSubmitRepo={handleSubmit}
        />
      </authzPermissionsContext.Provider>
    );

    expect(wrapper).toHaveLength(1);

    // Repository fields
    expect(wrapper.find({ name: "url" }).find("input")).toHaveLength(1);
    expect(wrapper.find({ name: "branch" }).find("input")).toHaveLength(1);
    expect(wrapper.find({ name: "environment" }).find("input")).toHaveLength(1);

    // Health Check
    expect(wrapper.find({ name: "includesHealthCheck" })).toHaveLength(0);

    wrapper.find(SwitchButton).at(0).simulate("click");

    expect(
      wrapper.find({ name: "includesHealthCheck" }).find("input")
    ).toHaveLength(1);

    // Filters
    expect(wrapper.find({ name: "gitignore" }).find("input")).toHaveLength(0);
  });

  it("should render envs modal", async (): Promise<void> => {
    expect.hasAssertions();

    const handleClose: jest.Mock = jest.fn();
    const handleSubmit: jest.Mock = jest.fn();
    const initialValues: IGitRootAttr = {
      __typename: "GitRoot",
      branch: "",
      cloningStatus: {
        message: "",
        status: "UNKNOWN",
      },
      environment: "",
      environmentUrls: [""],
      gitignore: [],
      id: "",
      includesHealthCheck: false,
      nickname: "",
      state: "ACTIVE",
      url: "https://gitlab.com/fluidattacks/product",
    };
    const wrapper: ReactWrapper = mount(
      <authzPermissionsContext.Provider
        value={
          new PureAbility([
            { action: "api_mutations_update_git_environments_mutate" },
          ])
        }
      >
        <ManagementModal
          initialValues={initialValues}
          nicknames={[]}
          onClose={handleClose}
          onSubmitEnvs={handleSubmit}
          onSubmitRepo={handleSubmit}
        />
      </authzPermissionsContext.Provider>
    );

    expect(wrapper).toHaveLength(1);

    wrapper.find("a").at(1).simulate("click", { button: 0 });
    const firstInput: ReactWrapper = wrapper
      .find({ name: "environmentUrls" })
      .find("input")
      .at(0);

    expect(firstInput).toHaveLength(1);

    firstInput.simulate("change", {
      target: {
        name: "environmentUrls[0]",
        value: "https://app.fluidattacks.com/",
      },
    });

    wrapper.find("form").simulate("submit");
    await wait(0);

    expect(handleSubmit).toHaveBeenCalledWith(
      {
        ...initialValues,
        environmentUrls: ["https://app.fluidattacks.com/"],
      },
      expect.anything()
    );

    const cancelButton: ReactWrapper = wrapper
      .find(ButtonToolbar)
      .find(Button)
      .at(0);

    cancelButton.simulate("click");

    expect(handleClose).toHaveBeenCalledWith(expect.anything());
  });
});
