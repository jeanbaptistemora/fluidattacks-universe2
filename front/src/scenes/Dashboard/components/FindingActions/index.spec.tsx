import { PureAbility } from "@casl/ability";
import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { authzContext } from "../../../../utils/authz/config";
import { FindingActions } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

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
    (window as typeof window & { userRole: string }).userRole = "analyst";
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding__do_delete_finding" },
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
        wrappingComponent: authzContext.Provider,
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
    (window as typeof window & { userRole: string }).userRole = "analyst";
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding__do_delete_finding" },
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
        wrappingComponent: authzContext.Provider,
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
    (window as typeof window & { userRole: string }).userRole = "admin";
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding__do_approve_draft" },
      { action: "backend_api_resolvers_finding__do_delete_finding" },
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
        wrappingComponent: authzContext.Provider,
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
    (window as typeof window & { userRole: string }).userRole = "admin";
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding__do_approve_draft" },
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
        wrappingComponent: authzContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      },
    );
    const buttons: ReactWrapper = wrapper.find("Button");
    const approveButton: ReactWrapper = buttons.at(1);

    expect(wrapper)
      .toHaveLength(1);
    expect(approveButton
      .text())
      .toContain("Approve");
    expect(approveButton.prop("disabled"))
      .toEqual(true);
  });
});
