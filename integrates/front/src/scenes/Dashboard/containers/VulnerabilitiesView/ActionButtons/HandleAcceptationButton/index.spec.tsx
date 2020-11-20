import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import waitForExpect from "wait-for-expect";

import {
  HandleAcceptationButton,
} from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons/HandleAcceptationButton/index";
import type {
  IHandleAcceptationButtonProps,
} from "scenes/Dashboard/containers/VulnerabilitiesView/ActionButtons/HandleAcceptationButton/types";
import { authzPermissionsContext } from "utils/authz/config";
import { translate } from "utils/translations/translate";

describe("HandleAcceptationButtons", () => {
  const openHandleAcceptation: jest.Mock = jest.fn();
  const baseMockedProps: IHandleAcceptationButtonProps = {
    canHandleAcceptation: true,
    isConfirmingZeroRisk: false,
    isEditing: true,
    isRejectingZeroRisk: false,
    isRequestingReattack: false,
    isRequestingZeroRisk: false,
    isVerifying: false,
    openHandleAcceptation,
  };

  it("should return a function", () => {
    expect(typeof (HandleAcceptationButton))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_handle_vulns_acceptation_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
        <HandleAcceptationButton {...baseMockedProps} />,
        {
          wrappingComponent: authzPermissionsContext.Provider,
          wrappingComponentProps: { value: mockedPermissions },
        },
    );
    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();
        expect(wrapper)
          .toHaveLength(1);
        expect(wrapper.find("Button"))
          .toHaveLength(0);

        wrapper.setProps({ isEditing: false });
        wrapper.update();
        const buttons: ReactWrapper = wrapper.find("Button");
        expect(buttons
          .filterWhere((button: ReactWrapper): boolean =>
          button
          .text()
          .includes(translate.t("search_findings.tab_vuln.buttons.handle_acceptation"))))
          .toHaveLength(1);

        buttons.simulate("click");
        expect(openHandleAcceptation)
          .toHaveBeenCalled();
      });
    });
  });
});
