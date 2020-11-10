import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { ActionButtons, IActionButtonsProps } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import { authzPermissionsContext } from "utils/authz/config";

describe("ActionButtons", () => {

  const baseMockedProps: IActionButtonsProps = {
    areVulnsSelected: false,
    isConfirmingZeroRisk: false,
    isEditing: false,
    isReattackRequestedInAllVuln: false,
    isRejectingZeroRisk: false,
    isRequestingReattack: false,
    isRequestingZeroRisk: false,
    isVerified: false,
    isVerifying: false,
    onConfirmZeroRisk: jest.fn(),
    onEdit: jest.fn(),
    onRejectZeroRisk: jest.fn(),
    onRequestReattack: jest.fn(),
    onRequestZeroRisk: jest.fn(),
    onVerify: jest.fn(),
    openModal: jest.fn(),
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
      isReattackRequestedInAllVuln: false,
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
        wrappingComponent: authzPermissionsContext.Provider,
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
          .includes("Reattack"));

    expect(requestButton)
      .toHaveLength(1);
    expect(buttons
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes("Edit")))
      .toHaveLength(1);

    requestButton.simulate("click");
    act(() => {
      wrapper.setProps({ isRequestingReattack: true });
      wrapper.update();
    });
    const { onRequestReattack } = requestMockProps;
    expect(onRequestReattack)
      .toHaveBeenCalled();

    buttons = wrapper.find("Button");
    requestButton = buttons
    .filterWhere((button: ReactWrapper): boolean =>
    button
    .text()
    .includes("Cancel"));
    expect(requestButton)
      .toHaveLength(1);
    expect(buttons
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes("Edit")))
      .toHaveLength(0);
  });
});
