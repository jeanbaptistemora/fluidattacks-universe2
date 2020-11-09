import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import * as React from "react";

import { FindingActions } from "scenes/Dashboard/components/FindingActions";
import { authzPermissionsContext } from "utils/authz/config";

describe("FindingActions", (): void => {

  it("should return a function", (): void => {
    expect(typeof (FindingActions))
      .toEqual("function");
  });

  it("should render no actions", (): void => {
    const wrapper: ReactWrapper = mount(
      <FindingActions
        hasVulns={false}
        hasSubmission={false}
        isDraft={false}
        loading={false}
        onApprove={jest.fn()}
        onDelete={jest.fn()}
        onReject={jest.fn()}
        onSubmit={jest.fn()}
      />,
    );
    const buttons: ReactWrapper = wrapper.find("button");

    expect(wrapper)
      .toHaveLength(1);
    expect(buttons)
      .toHaveLength(0);
  });

  it("should render analyst finding actions", (): void => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_delete_finding_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <FindingActions
        hasVulns={false}
        hasSubmission={true}
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
      },
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper)
      .toHaveLength(1);
    expect(buttons)
      .toHaveLength(1);
    expect(buttons
      .text())
      .toContain("Delete");
  });

  it("should render author draft actions", (): void => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_delete_finding_mutate" },
      { action: "backend_api_resolvers_finding__do_submit_draft" },
    ]);
    const wrapper: ReactWrapper = mount(
      <FindingActions
        hasVulns={false}
        hasSubmission={false}
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
      },
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper)
      .toHaveLength(1);
    expect(buttons)
      .toHaveLength(2);
    expect(buttons
      .at(0)
      .text())
      .toContain("Submit");
    expect(buttons
      .at(1)
      .text())
      .toContain("Delete");
  });

  it("should render approver draft actions", (): void => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_approve_draft_mutate" },
      { action: "backend_api_mutations_delete_finding_mutate" },
      { action: "backend_api_resolvers_finding__do_reject_draft" },
    ]);
    const wrapper: ReactWrapper = mount(
      <FindingActions
        hasVulns={true}
        hasSubmission={true}
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
      },
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper)
      .toHaveLength(1);
    expect(buttons)
      .toHaveLength(3);
    expect(buttons
      .at(0)
      .text())
      .toContain("Approve");
    expect(buttons
      .at(1)
      .text())
      .toContain("Reject");
    expect(buttons
      .at(2)
      .text())
      .toContain("Delete");
  });

  it("should disable approve button", (): void => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_approve_draft_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <FindingActions
        hasVulns={false}
        hasSubmission={false}
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
      },
    );
    const buttons: ReactWrapper = wrapper.find("Button");
    const approveButton: ReactWrapper = buttons.at(0);

    expect(wrapper)
      .toHaveLength(1);
    expect(approveButton
      .text())
      .toContain("Approve");
    expect(approveButton.prop("disabled"))
      .toEqual(true);
  });
});
