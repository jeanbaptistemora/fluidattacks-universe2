import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { useTranslation } from "react-i18next";
import { ActionButtons, IActionButtonsProps } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import { authzPermissionsContext } from "utils/authz/config";

describe("ActionButtons", () => {
  (window as typeof window & { userEmail: string }).userEmail = "test@fluidattacks.com";

  const baseMockedProps: IActionButtonsProps = {
    areVulnsSelected: false,
    canHandleAcceptation: false,
    isConfirmingZeroRisk: false,
    isEditing: false,
    isReattackRequestedInAllVuln: false,
    isRejectingZeroRisk: false,
    isRequestingReattack: false,
    isVerified: false,
    isVerifying: false,
    onConfirmZeroRisk: jest.fn(),
    onEdit: jest.fn(),
    onRejectZeroRisk: jest.fn(),
    onRequestReattack: jest.fn(),
    onVerify: jest.fn(),
    openHandleAcceptation: jest.fn(),
    openModal: jest.fn(),
    openUpdateZeroRiskModal: jest.fn(),
    state: "open",
    subscription: "",
  };

  it("should return a function", () => {
    expect(typeof (ActionButtons))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const { t } = useTranslation();
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
          .includes(t("search_findings.tab_description.editable.text"))))
      .toHaveLength(1);
  });

  it("should render request verification", async () => {
    const { t } = useTranslation();
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
          .includes(t("search_findings.tab_description.request_verify.tex")));

    expect(requestButton)
      .toHaveLength(1);
    expect(buttons
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("search_findings.tab_description.editable.text"))))
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
    .includes(t("search_findings.tab_description.cancel_verify")));
    expect(requestButton)
      .toHaveLength(1);
    expect(buttons
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes("Edit")))
      .toHaveLength(0);
  });

  it("should render confirm zero risk", async () => {
    const { t } = useTranslation();
    const confirmZeroRiskMockProps: IActionButtonsProps = {
      ...baseMockedProps,
    };
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_confirm_zero_risk_vuln_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons {...confirmZeroRiskMockProps} />,
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

    let confirmZeroRiskButton: ReactWrapper = buttons
    .filterWhere((button: ReactWrapper): boolean =>
      button
        .text()
        .includes("Confirm zero risk"));
    expect(confirmZeroRiskButton)
      .toHaveLength(1);

    const editButton: ReactWrapper = buttons
      .filterWhere((button: ReactWrapper): boolean =>
        button
        .text()
        .includes(t("search_findings.tab_description.editable.text")));
    expect(editButton)
      .toHaveLength(1);

    confirmZeroRiskButton.simulate("click");

    act(() => {
      wrapper.setProps({ isConfirmingZeroRisk: true });
      wrapper.update();
    });

    const { onConfirmZeroRisk } = confirmZeroRiskMockProps;
    expect(onConfirmZeroRisk)
      .toHaveBeenCalled();

    buttons = wrapper.find("Button");
    expect(buttons)
      .toHaveLength(2);

    confirmZeroRiskButton = buttons
      .filterWhere((button: ReactWrapper): boolean =>
        button
        .text()
        .includes("Confirm zero risk"));
    expect(confirmZeroRiskButton)
      .toHaveLength(1);

    const cancelButton: ReactWrapper = buttons
    .filterWhere((button: ReactWrapper): boolean =>
      button
      .text()
      .includes("Cancel"));
    expect(cancelButton)
      .toHaveLength(1);
  });

  it("should render reject zero risk", async () => {
    const { t } = useTranslation();
    const rejectZeroRiskMockProps: IActionButtonsProps = {
      ...baseMockedProps,
    };
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_reject_zero_risk_vuln_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons {...rejectZeroRiskMockProps} />,
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

    let rejectZeroRiskButton: ReactWrapper = buttons
    .filterWhere((button: ReactWrapper): boolean =>
      button
        .text()
        .includes(t("search_findings.tab_description.reject_zero_risk.text")));
    expect(rejectZeroRiskButton)
      .toHaveLength(1);

    const editButton: ReactWrapper = buttons
      .filterWhere((button: ReactWrapper): boolean =>
        button
        .text()
        .includes(t("search_findings.tab_description.editable.text")));
    expect(editButton)
      .toHaveLength(1);

    rejectZeroRiskButton.simulate("click");

    act(() => {
      wrapper.setProps({ isRejectingZeroRisk: true });
      wrapper.update();
    });

    const { onRejectZeroRisk } = rejectZeroRiskMockProps;
    expect(onRejectZeroRisk)
      .toHaveBeenCalled();

    buttons = wrapper.find("Button");
    expect(buttons)
      .toHaveLength(2);

    rejectZeroRiskButton = buttons
      .filterWhere((button: ReactWrapper): boolean =>
        button
        .text()
        .includes(t("search_findings.tab_description.reject_zero_risk.text")));
    expect(rejectZeroRiskButton)
      .toHaveLength(1);

    const cancelButton: ReactWrapper = buttons
    .filterWhere((button: ReactWrapper): boolean =>
      button
      .text()
      .includes(t("search_findings.tab_description.cancel_rejecting_zero_risk")));
    expect(cancelButton)
      .toHaveLength(1);
  });
});
