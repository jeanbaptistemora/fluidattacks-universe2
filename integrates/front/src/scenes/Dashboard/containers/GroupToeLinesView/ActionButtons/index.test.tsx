import { PureAbility } from "@casl/ability";
import { render, screen } from "@testing-library/react";
import React from "react";

import { ActionButtons } from ".";
import { authzPermissionsContext } from "utils/authz/config";

describe("ToelinesActionButtons", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toBe("function");
  });

  it("should not display the edition button without permissions", (): void => {
    expect.hasAssertions();

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <ActionButtons
          areToeLinesDatasSelected={true}
          isEditing={false}
          isInternal={true}
          onEdit={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("should hide the edition button for the external view", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_toe_lines_attacked_lines_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons
          areToeLinesDatasSelected={true}
          isEditing={false}
          isInternal={false}
          onEdit={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("should display the edition button", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_toe_lines_attacked_lines_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons
          areToeLinesDatasSelected={true}
          isEditing={false}
          isInternal={true}
          onEdit={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(
      screen.queryByText("group.toe.lines.actionButtons.editButton.text")
    ).toBeInTheDocument();
  });
});
