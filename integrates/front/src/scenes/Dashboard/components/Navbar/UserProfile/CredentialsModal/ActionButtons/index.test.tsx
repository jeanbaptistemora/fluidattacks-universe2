import { PureAbility } from "@casl/ability";
import { render, screen } from "@testing-library/react";
import React from "react";

import { ActionButtons } from ".";
import { authzPermissionsContext } from "utils/authz/config";

describe("credentialsModalButtons", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toBe("function");
  });

  it("should not display the edition button without permissions", (): void => {
    expect.hasAssertions();

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <ActionButtons
          isAdding={false}
          isEditingSecrets={false}
          onAdd={jest.fn()}
          onEditSecrets={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(
      screen.queryByText(
        "profile.credentialsModal.actionButtons.editSecretsButton.text"
      )
    ).not.toBeInTheDocument();
  });

  it("should display the edit secrets button", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "front_can_edit_credentials_secrets_in_bulk" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons
          isAdding={false}
          isEditingSecrets={false}
          onAdd={jest.fn()}
          onEditSecrets={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(
      screen.queryByText(
        "profile.credentialsModal.actionButtons.editSecretsButton.text"
      )
    ).toBeInTheDocument();
  });

  it("should display the add button", (): void => {
    expect.hasAssertions();

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <ActionButtons
          isAdding={false}
          isEditingSecrets={false}
          onAdd={jest.fn()}
          onEditSecrets={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(
      screen.queryByText(
        "profile.credentialsModal.actionButtons.addButton.text"
      )
    ).toBeInTheDocument();
  });
});
