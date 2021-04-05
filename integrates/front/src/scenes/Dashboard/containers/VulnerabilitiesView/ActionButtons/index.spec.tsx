import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { useTranslation } from "react-i18next";

import { ActionButtons } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import { authzPermissionsContext } from "utils/authz/config";

describe("ActionButtons", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toStrictEqual("function");
  });

  it("should render a component without permissions", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areVulnsSelected={false}
        isEditing={false}
        isFindingReleased={true}
        isReattackRequestedInAllVuln={false}
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
        wrappingComponentProps: { value: new PureAbility([]) },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(0);
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_update_vulns_treatment_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areVulnsSelected={false}
        isEditing={false}
        isFindingReleased={true}
        isReattackRequestedInAllVuln={false}
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

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(1);
    expect(
      buttons.filterWhere((button: ReactWrapper): boolean =>
        button.text().includes(t("searchFindings.tabVuln.buttons.edit"))
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
          "backend_api_mutations_request_verification_vulnerability_mutate",
      },
      { action: "backend_api_mutations_update_vulns_treatment_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areVulnsSelected={false}
        isEditing={false}
        isFindingReleased={true}
        isReattackRequestedInAllVuln={false}
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
          .includes(t("searchFindings.tabDescription.requestVerify.tex"))
    );

    expect(requestButton).toHaveLength(1);
    expect(
      buttons.filterWhere((button: ReactWrapper): boolean =>
        button.text().includes(t("searchFindings.tabVuln.buttons.edit"))
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
        button.text().includes(t("searchFindings.tabDescription.cancelVerify"))
      );

    expect(cancelRequestButton).toHaveLength(1);
    expect(
      wrapper
        .find("Button")
        .filterWhere((button: ReactWrapper): boolean =>
          button.text().includes(t("searchFindings.tabVuln.buttons.edit"))
        )
    ).toHaveLength(0);
  });
});
