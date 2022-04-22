import { PureAbility } from "@casl/ability";
import { render, screen } from "@testing-library/react";
import React from "react";

import { ActionButtons } from ".";
import { authzPermissionsContext } from "utils/authz/config";

describe("ToeInputsActionButtons", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toBe("function");
  });

  it("should not display the edition button without permissions", (): void => {
    expect.hasAssertions();

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <ActionButtons
          areInputsSelected={true}
          isAdding={false}
          isEditing={false}
          isInternal={true}
          onAdd={jest.fn()}
          onEdit={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("should hide the addition button for the external view", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_toe_input_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons
          areInputsSelected={true}
          isAdding={false}
          isEditing={false}
          isInternal={false}
          onAdd={jest.fn()}
          onEdit={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("should display the addition button", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_toe_input_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons
          areInputsSelected={true}
          isAdding={false}
          isEditing={false}
          isInternal={true}
          onAdd={jest.fn()}
          onEdit={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(
      screen.queryByText("group.toe.inputs.actionButtons.addButton.text")
    ).toBeInTheDocument();
  });

  it("should display the edition button", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_toe_input_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons
          areInputsSelected={true}
          isAdding={false}
          isEditing={false}
          isInternal={true}
          onAdd={jest.fn()}
          onEdit={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(
      screen.queryByText("group.toe.inputs.actionButtons.editButton.text")
    ).toBeInTheDocument();
  });
});
