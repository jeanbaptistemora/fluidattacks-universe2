import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { authzContext } from "../../../../../utils/authz/config";
import { ActionButtons, IActionButtonsProps } from "./index";

describe("ActionButtons", () => {

  const baseMockedProps: IActionButtonsProps = {
    isEditing: false,
    isPristine: false,
    isRemediated: false,
    isRequestingVerify: false,
    isVerified: false,
    isVerifying: false,
    lastTreatment: {
      acceptanceDate: "",
      acceptanceStatus: "",
      date: "",
      justification: "",
      treatment: "",
      user: "",
    },
    onApproveAcceptation: jest.fn(),
    onEdit: jest.fn(),
    onRejectAcceptation: jest.fn(),
    onRequestVerify: jest.fn(),
    onUpdate: jest.fn(),
    onVerify: jest.fn(),
    state: "open",
    subscription: "",
  };

  it("should return a function", () => {
    expect(typeof (ActionButtons))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <ActionButtons {...baseMockedProps} />,
    );
    expect(wrapper)
      .toHaveLength(1);
    const buttons: ReactWrapper = wrapper.find("Button");
    expect(buttons)
      .toHaveLength(1);
    expect(buttons
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes("Edit")))
      .toHaveLength(1);
  });

  it("should render request verification", async () => {
    const requestMockProps: IActionButtonsProps = {
      ...baseMockedProps,
      isEditing: false,
      isRemediated: false,
      isVerified: false,
      state: "open",
      subscription: "continuous",
    };
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_vulnerability__do_request_verification_vuln" },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons {...requestMockProps} />,
      {
        wrappingComponent: authzContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      },
    );
    expect(wrapper)
      .toHaveLength(1);
    let buttons: ReactWrapper = wrapper.find("Button");
    expect(buttons)
      .toHaveLength(2);
    let requestButton: ReactWrapper = buttons
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes("Request"));
    expect(requestButton)
      .toHaveLength(1);
    requestButton.simulate("click");
    act(() => {
      wrapper.setProps({ isRequestingVerify: true });
      wrapper.update();
    });
    const { onRequestVerify } = requestMockProps;
    expect(onRequestVerify)
      .toHaveBeenCalled();
    buttons = wrapper.find("Button");
    requestButton = buttons
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes("Cancel"));
    expect(requestButton)
      .toHaveLength(1);
  });
});
