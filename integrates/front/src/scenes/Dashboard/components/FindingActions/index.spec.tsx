import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";

import { FindingActions } from "scenes/Dashboard/components/FindingActions";
import { authzPermissionsContext } from "utils/authz/config";

describe("FindingActions", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof FindingActions).toStrictEqual("function");
  });

  it("should render no actions", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <FindingActions
        hasSubmission={false}
        hasVulns={false}
        isDraft={false}
        loading={false}
        onApprove={jest.fn()}
        onDelete={jest.fn()}
        onReject={jest.fn()}
        onSubmit={jest.fn()}
      />
    );
    const buttons: ReactWrapper = wrapper.find("button");

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(0);
  });

  it("should render hacker finding actions", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_remove_finding_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <FindingActions
        hasSubmission={true}
        hasVulns={false}
        isDraft={false}
        loading={false}
        onApprove={jest.fn()}
        onDelete={jest.fn()}
        onReject={jest.fn()}
        onSubmit={jest.fn()}
      />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(0);
  });

  it("should render author draft actions", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_remove_finding_mutate" },
      { action: "api_mutations_submit_draft_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <FindingActions
        hasSubmission={false}
        hasVulns={false}
        isDraft={true}
        loading={false}
        onApprove={jest.fn()}
        onDelete={jest.fn()}
        onReject={jest.fn()}
        onSubmit={jest.fn()}
      />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(2);
    expect(buttons.at(0).text()).toContain("Submit");
    expect(buttons.at(1).text()).toContain("Delete");
  });

  it("should render approver draft actions", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_approve_draft_mutate" },
      { action: "api_mutations_remove_finding_mutate" },
      { action: "api_mutations_reject_draft_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <FindingActions
        hasSubmission={true}
        hasVulns={true}
        isDraft={true}
        loading={false}
        onApprove={jest.fn()}
        onDelete={jest.fn()}
        onReject={jest.fn()}
        onSubmit={jest.fn()}
      />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");
    const BUTTONS_LENGTH: number = 3;

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(BUTTONS_LENGTH);
    expect(buttons.at(0).text()).toContain("Approve");
    expect(buttons.at(1).text()).toContain("Reject");
    expect(buttons.at(2).text()).toContain("Delete");
  });

  it("should disable approve button", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_approve_draft_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <FindingActions
        hasSubmission={false}
        hasVulns={false}
        isDraft={true}
        loading={false}
        onApprove={jest.fn()}
        onDelete={jest.fn()}
        onReject={jest.fn()}
        onSubmit={jest.fn()}
      />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");
    const approveButton: ReactWrapper = buttons.at(0);

    expect(wrapper).toHaveLength(1);
    expect(approveButton.text()).toContain("Approve");
    expect(approveButton.prop("disabled")).toStrictEqual(true);
  });
});
