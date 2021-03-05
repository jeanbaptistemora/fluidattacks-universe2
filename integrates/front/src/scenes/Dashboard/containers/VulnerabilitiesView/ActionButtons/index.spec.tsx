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
      />
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(1);
    expect(
      buttons.filterWhere((button: ReactWrapper): boolean =>
        button.text().includes(t("search_findings.tab_vuln.buttons.edit"))
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
          .includes(t("search_findings.tab_description.request_verify.tex"))
    );

    expect(requestButton).toHaveLength(1);
    expect(
      buttons.filterWhere((button: ReactWrapper): boolean =>
        button.text().includes(t("search_findings.tab_vuln.buttons.edit"))
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
          button.text().includes(t("search_findings.tab_vuln.buttons.edit"))
        )
    ).toHaveLength(0);
  });
});
