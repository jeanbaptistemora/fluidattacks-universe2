import { PureAbility } from "@casl/ability";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { useTranslation } from "react-i18next";

import { HandleAcceptanceButton } from ".";
import { authzPermissionsContext } from "utils/authz/config";

describe("HandleAcceptanceButtons", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof HandleAcceptanceButton).toStrictEqual("function");
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const openHandleAcceptance: jest.Mock = jest.fn();
    const handleAcceptanceButtonText: string = t(
      "searchFindings.tabVuln.buttons.handleAcceptance"
    );
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_handle_vulnerabilities_acceptance_mutate" },
    ]);
    const { rerender } = render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <HandleAcceptanceButton
          areVulnerabilitiesPendingToAcceptance={true}
          isEditing={true}
          isRequestingReattack={false}
          isVerifying={false}
          openHandleAcceptance={openHandleAcceptance}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryAllByText(handleAcceptanceButtonText)).toHaveLength(0);

    rerender(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <HandleAcceptanceButton
          areVulnerabilitiesPendingToAcceptance={false}
          isEditing={false}
          isRequestingReattack={false}
          isVerifying={false}
          openHandleAcceptance={openHandleAcceptance}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryAllByText(handleAcceptanceButtonText)).toHaveLength(0);

    rerender(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <HandleAcceptanceButton
          areVulnerabilitiesPendingToAcceptance={true}
          isEditing={false}
          isRequestingReattack={false}
          isVerifying={false}
          openHandleAcceptance={openHandleAcceptance}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.getByText(handleAcceptanceButtonText)).toBeInTheDocument();

    userEvent.click(screen.getByText(handleAcceptanceButtonText));

    expect(openHandleAcceptance).toHaveBeenCalledTimes(1);
  });
});
