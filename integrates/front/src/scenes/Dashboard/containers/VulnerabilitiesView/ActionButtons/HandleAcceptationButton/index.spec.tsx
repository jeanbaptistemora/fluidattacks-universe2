import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { useTranslation } from "react-i18next";
import waitForExpect from "wait-for-expect";

import { HandleAcceptationButton } from ".";
import { authzPermissionsContext } from "utils/authz/config";

describe("HandleAcceptationButtons", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof HandleAcceptationButton).toStrictEqual("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const openHandleAcceptation: jest.Mock = jest.fn();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_handle_vulnerabilities_acceptation_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <HandleAcceptationButton
        areVulnerabilitiesPendingToAcceptation={true}
        isEditing={true}
        isRequestingReattack={false}
        isVerifying={false}
        openHandleAcceptation={openHandleAcceptation}
      />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
        expect(wrapper.find("Button")).toHaveLength(0);

        wrapper.setProps({
          areVulnerabilitiesPendingToAcceptation: false,
          isEditing: false,
        });
        wrapper.update();

        expect(wrapper.find("Button")).toHaveLength(0);

        wrapper.setProps({ areVulnerabilitiesPendingToAcceptation: true });
        wrapper.update();
        const buttons: ReactWrapper = wrapper.find("Button");

        expect(
          buttons.filterWhere((button: ReactWrapper): boolean =>
            button
              .text()
              .includes(t("searchFindings.tabVuln.buttons.handleAcceptation"))
          )
        ).toHaveLength(1);

        buttons.simulate("click");

        expect(openHandleAcceptation).toHaveBeenCalledTimes(1);
      });
    });
  });
});
