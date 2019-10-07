import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import * as React from "react";
import { Button } from "react-bootstrap";
import { FindingActions } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("FindingActions", (): void => {

  it("should return a function", (): void => {
    expect(typeof (FindingActions))
      .toEqual("function");
  });

  it("should render no actions", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <FindingActions
        hasVulns={false}
        hasSubmission={false}
        isAuthor={false}
        isDraft={false}
        loading={false}
        onApprove={jest.fn()}
        onDelete={jest.fn()}
        onReject={jest.fn()}
        onSubmit={jest.fn()}
      />,
    );
    const buttons: ShallowWrapper = wrapper.find("button");

    expect(wrapper)
      .toHaveLength(1);
    expect(buttons)
      .toHaveLength(0);
  });

  it("should render analyst finding actions", (): void => {
    (window as typeof window & { userRole: string }).userRole = "analyst";
    const wrapper: ShallowWrapper = shallow(
      <FindingActions
        hasVulns={false}
        hasSubmission={true}
        isAuthor={false}
        isDraft={false}
        loading={false}
        onApprove={jest.fn()}
        onDelete={jest.fn()}
        onReject={jest.fn()}
        onSubmit={jest.fn()}
      />,
    );
    const buttons: ShallowWrapper = wrapper.find("button");

    expect(wrapper)
      .toHaveLength(1);
    expect(buttons)
      .toHaveLength(1);
    expect(buttons
      .children()
      .at(1)
      .text())
      .toContain("Delete");
  });

  it("should render author draft actions", (): void => {
    (window as typeof window & { userRole: string }).userRole = "analyst";
    const wrapper: ShallowWrapper = shallow(
      <FindingActions
        hasVulns={false}
        hasSubmission={false}
        isAuthor={true}
        isDraft={true}
        loading={false}
        onApprove={jest.fn()}
        onDelete={jest.fn()}
        onReject={jest.fn()}
        onSubmit={jest.fn()}
      />,
    );
    const buttons: ShallowWrapper = wrapper.find("button");

    expect(wrapper)
      .toHaveLength(1);
    expect(buttons)
      .toHaveLength(2);
    expect(buttons
      .at(0)
      .children()
      .at(0)
      .text())
      .toContain("Submit");
    expect(buttons
      .at(1)
      .children()
      .at(1)
      .text())
      .toContain("Delete");
  });

  it("should render approver draft actions", (): void => {
    (window as typeof window & { userRole: string }).userRole = "admin";
    const wrapper: ShallowWrapper = shallow(
      <FindingActions
        hasVulns={true}
        hasSubmission={true}
        isAuthor={false}
        isDraft={true}
        loading={false}
        onApprove={jest.fn()}
        onDelete={jest.fn()}
        onReject={jest.fn()}
        onSubmit={jest.fn()}
      />,
    );
    const buttons: ShallowWrapper = wrapper.find("button");

    expect(wrapper)
      .toHaveLength(1);
    expect(buttons)
      .toHaveLength(3);
    expect(buttons
      .at(0)
      .children()
      .at(1)
      .text())
      .toContain("Approve");
    expect(buttons
      .at(1)
      .children()
      .at(0)
      .text())
      .toContain("Reject");
    expect(buttons
      .at(2)
      .children()
      .at(1)
      .text())
      .toContain("Delete");
  });

  it("should disable approve button", (): void => {
    (window as typeof window & { userRole: string }).userRole = "admin";
    const wrapper: ShallowWrapper = shallow(
      <FindingActions
        hasVulns={false}
        hasSubmission={false}
        isAuthor={false}
        isDraft={true}
        loading={false}
        onApprove={jest.fn()}
        onDelete={jest.fn()}
        onReject={jest.fn()}
        onSubmit={jest.fn()}
      />,
    );
    const buttons: ShallowWrapper = wrapper.find("button");
    const approveButton: ShallowWrapper<Button.ButtonProps> = buttons
      .at(0);

    expect(wrapper)
      .toHaveLength(1);
    expect(approveButton
      .children()
      .at(1)
      .text())
      .toContain("Approve");
    expect(approveButton.props().disabled)
      .toEqual(true);
  });
});
