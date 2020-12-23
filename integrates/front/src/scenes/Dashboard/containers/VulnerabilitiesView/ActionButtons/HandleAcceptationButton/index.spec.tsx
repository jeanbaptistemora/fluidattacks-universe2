import { HandleAcceptationButton } from ".";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { act } from "react-dom/test-utils";
import { authzPermissionsContext } from "utils/authz/config";
import { mount } from "enzyme";
import { useTranslation } from "react-i18next";
import waitForExpect from "wait-for-expect";

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
      { action: "backend_api_mutations_handle_vulns_acceptation_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <HandleAcceptationButton
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
    await act(
      async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper).toHaveLength(1);
          expect(wrapper.find("Button")).toHaveLength(0);

          wrapper.setProps({ isEditing: false });
          wrapper.update();
          const buttons: ReactWrapper = wrapper.find("Button");

          expect(
            buttons.filterWhere((button: ReactWrapper): boolean =>
              button
                .text()
                .includes(
                  t("search_findings.tab_vuln.buttons.handle_acceptation")
                )
            )
          ).toHaveLength(1);

          buttons.simulate("click");

          expect(openHandleAcceptation).toHaveBeenCalledTimes(1);
        });
      }
    );
  });
});
