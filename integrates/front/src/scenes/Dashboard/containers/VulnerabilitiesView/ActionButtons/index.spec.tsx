import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { useTranslation } from "react-i18next";

import { ActionButtons } from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";
import { msgInfo } from "utils/notifications";
import { translate } from "utils/translations/translate";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgInfo").mockImplementation();

  return mockedNotifications;
});

describe("ActionButtons", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toStrictEqual("function");
  });

  it("should render a component without permissions", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areVulnerabilitiesPendingToAcceptation={true}
        areVulnsSelected={false}
        isEditing={false}
        isFindingReleased={true}
        isOpen={false}
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
      { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areVulnerabilitiesPendingToAcceptation={true}
        areVulnsSelected={false}
        isEditing={false}
        isFindingReleased={true}
        isOpen={false}
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
      { action: "api_mutations_request_vulnerabilities_verification_mutate" },
      { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    ]);
    const mockedServices: PureAbility<string> = new PureAbility([
      { action: "is_continuous" },
    ]);
    const contextWrapper: React.FC = ({ children }): JSX.Element => (
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <authzGroupContext.Provider value={mockedServices}>
          {children}
        </authzGroupContext.Provider>
      </authzPermissionsContext.Provider>
    );
    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areVulnerabilitiesPendingToAcceptation={true}
        areVulnsSelected={false}
        isEditing={false}
        isFindingReleased={true}
        isOpen={false}
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
      { wrappingComponent: contextWrapper }
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
      wrapper.setProps({ isOpen: false, isRequestingReattack: true });
      wrapper.update();
    });

    expect(onRequestReattack).toHaveBeenCalledTimes(1);
    expect(msgInfo).toHaveBeenCalledWith(
      translate.t("searchFindings.tabVuln.info.text"),
      translate.t("searchFindings.tabVuln.info.title"),
      true
    );

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

    cancelRequestButton.simulate("click");
    act((): void => {
      wrapper.setProps({ isOpen: false, isRequestingReattack: false });
      wrapper.update();
    });

    expect(
      wrapper
        .find("Button")
        .filterWhere((button: ReactWrapper): boolean =>
          button
            .text()
            .includes(t("searchFindings.tabDescription.cancelVerify"))
        )
    ).toHaveLength(0);
    expect(msgInfo).toHaveBeenCalledWith(
      translate.t("searchFindings.tabVuln.info.text"),
      translate.t("searchFindings.tabVuln.info.title"),
      false
    );
  });
});
