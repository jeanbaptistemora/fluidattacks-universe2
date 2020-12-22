import { ActionButtons } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { act } from "react-dom/test-utils";
import { authzPermissionsContext } from "utils/authz/config";
import { mount } from "enzyme";
import { useTranslation } from "react-i18next";

describe("ActionButtons", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toStrictEqual("function");
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areVulnsSelected={false}
        isConfirmingZeroRisk={false}
        isEditing={false}
        isReattackRequestedInAllVuln={false}
        isRejectingZeroRisk={false}
        isRequestingReattack={false}
        isVerified={false}
        isVerifying={false}
        onEdit={jest.fn()}
        onRequestReattack={jest.fn()}
        onVerify={jest.fn()}
        openHandleAcceptation={jest.fn()}
        openModal={jest.fn()}
        state={"open"}
        subscription={""}
      />
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(1);
    expect(
      buttons.filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("search_findings.tab_description.editable.text"))
      )
    ).toHaveLength(1);
  });

  it("should render request verification", (): void => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const onRequestReattack: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      {
        action:
          "backend_api_resolvers_vulnerability__do_request_verification_vuln",
      },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areVulnsSelected={false}
        isConfirmingZeroRisk={false}
        isEditing={false}
        isReattackRequestedInAllVuln={false}
        isRejectingZeroRisk={false}
        isRequestingReattack={false}
        isVerified={false}
        isVerifying={false}
        onEdit={jest.fn()}
        onRequestReattack={onRequestReattack}
        onVerify={jest.fn()}
        openHandleAcceptation={jest.fn()}
        openModal={jest.fn()}
        state={"open"}
        subscription={"continuous"}
      />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(2);

    const requestButton: ReactWrapper = buttons.filterWhere(
      (button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("search_findings.tab_description.request_verify.tex"))
    );

    expect(requestButton).toHaveLength(1);
    expect(
      buttons.filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("search_findings.tab_description.editable.text"))
      )
    ).toHaveLength(1);

    requestButton.simulate("click");

    act((): void => {
      wrapper.setProps({ isRequestingReattack: true });
      wrapper.update();
    });

    expect(onRequestReattack).toHaveBeenCalledTimes(1);

    const cancelRequestButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("search_findings.tab_description.cancel_verify"))
      );

    expect(cancelRequestButton).toHaveLength(1);
    expect(
      wrapper
        .find("Button")
        .filterWhere((button: ReactWrapper): boolean =>
          button
            .text()
            .includes(t("search_findings.tab_description.editable.text"))
        )
    ).toHaveLength(0);
  });

  // eslint-disable-next-line jest/no-disabled-tests
  it.skip("should render confirm zero risk", (): void => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const onConfirmZeroRisk: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_confirm_zero_risk_vuln_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areVulnsSelected={false}
        isConfirmingZeroRisk={false}
        isEditing={false}
        isReattackRequestedInAllVuln={false}
        isRejectingZeroRisk={false}
        isRequestingReattack={false}
        isVerified={false}
        isVerifying={false}
        onEdit={jest.fn()}
        onRequestReattack={jest.fn()}
        onVerify={jest.fn()}
        openHandleAcceptation={jest.fn()}
        openModal={jest.fn()}
        state={"open"}
        subscription={""}
      />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");
    const expectedButtons: number = 3;

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(expectedButtons);

    const confirmZeroRiskButton: ReactWrapper = buttons.filterWhere(
      (button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("search_findings.tab_description.confirm_zero_risk.text"))
    );

    expect(confirmZeroRiskButton).toHaveLength(1);

    const editButton: ReactWrapper = buttons.filterWhere(
      (button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("search_findings.tab_description.editable.text"))
    );

    expect(editButton).toHaveLength(1);

    confirmZeroRiskButton.simulate("click");

    act((): void => {
      wrapper.setProps({ isConfirmingZeroRisk: true });
      wrapper.update();
    });

    expect(onConfirmZeroRisk).toHaveBeenCalledTimes(1);
    expect(wrapper.find("Button")).toHaveLength(2);
    expect(confirmZeroRiskButton).toHaveLength(1);

    const cancelButton: ReactWrapper = buttons.filterWhere(
      (button: ReactWrapper): boolean =>
        button
          .text()
          .includes(
            t("search_findings.tab_description.cancel_confirming_zero_risk")
          )
    );

    expect(cancelButton).toHaveLength(1);
  });

  // eslint-disable-next-line jest/no-disabled-tests
  it.skip("should render reject zero risk", (): void => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const onRejectZeroRisk: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_reject_zero_risk_vuln_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areVulnsSelected={false}
        isConfirmingZeroRisk={false}
        isEditing={false}
        isReattackRequestedInAllVuln={false}
        isRejectingZeroRisk={false}
        isRequestingReattack={false}
        isVerified={false}
        isVerifying={false}
        onEdit={jest.fn()}
        onRequestReattack={jest.fn()}
        onVerify={jest.fn()}
        openHandleAcceptation={jest.fn()}
        openModal={jest.fn()}
        state={"open"}
        subscription={""}
      />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const expectedButtons: number = 3;

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find("Button")).toHaveLength(expectedButtons);

    const rejectZeroRiskButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("search_findings.tab_description.reject_zero_risk.text"))
      );

    expect(rejectZeroRiskButton).toHaveLength(1);

    const editButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("search_findings.tab_description.editable.text"))
      );

    expect(editButton).toHaveLength(1);

    rejectZeroRiskButton.simulate("click");

    act((): void => {
      wrapper.setProps({ isRejectingZeroRisk: true });
      wrapper.update();
    });

    expect(onRejectZeroRisk).toHaveBeenCalledTimes(1);
    expect(wrapper.find("Button")).toHaveLength(2);
    expect(rejectZeroRiskButton).toHaveLength(1);

    const cancelButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes(
            t("search_findings.tab_description.cancel_rejecting_zero_risk")
          )
      );

    expect(cancelButton).toHaveLength(1);
  });
});
