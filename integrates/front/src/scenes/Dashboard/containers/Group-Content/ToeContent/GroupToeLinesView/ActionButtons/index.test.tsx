import { PureAbility } from "@casl/ability";
import { render, screen } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

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
        <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
          <Route path={"/:groupName/surface/lines"}>
            <ActionButtons
              areToeLinesDatasSelected={true}
              isAdding={false}
              isEditing={false}
              isInternal={true}
              isVerifying={false}
              onAdd={jest.fn()}
              onEdit={jest.fn()}
              onVerify={jest.fn()}
            />
          </Route>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("should hide the edition button for the external view", (): void => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_toe_lines_attacked_lines_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
          <Route path={"/:groupName/surface/lines"}>
            <ActionButtons
              areToeLinesDatasSelected={true}
              isAdding={false}
              isEditing={false}
              isInternal={false}
              isVerifying={false}
              onAdd={jest.fn()}
              onEdit={jest.fn()}
              onVerify={jest.fn()}
            />
          </Route>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("should display the edition button", (): void => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_toe_lines_attacked_lines_mutate" },
    ]);

    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
          <Route path={"/:groupName/surface/lines"}>
            <ActionButtons
              areToeLinesDatasSelected={true}
              isAdding={false}
              isEditing={false}
              isInternal={true}
              isVerifying={false}
              onAdd={jest.fn()}
              onEdit={jest.fn()}
              onVerify={jest.fn()}
            />
          </Route>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    expect(
      screen.queryByText("group.toe.lines.actionButtons.editButton.text")
    ).toBeInTheDocument();
  });

  it("should display the addition button", (): void => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_toe_lines_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
          <Route path={"/:groupName/surface/lines"}>
            <ActionButtons
              areToeLinesDatasSelected={true}
              isAdding={false}
              isEditing={false}
              isInternal={true}
              isVerifying={false}
              onAdd={jest.fn()}
              onEdit={jest.fn()}
              onVerify={jest.fn()}
            />
          </Route>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(
      screen.queryByText("group.toe.lines.actionButtons.addButton.text")
    ).toBeInTheDocument();
  });

  it("should display the verify button", (): void => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_toe_lines_attacked_lines_mutate" },
    ]);

    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
          <Route path={"/:groupName/surface/lines"}>
            <ActionButtons
              areToeLinesDatasSelected={true}
              isAdding={false}
              isEditing={false}
              isInternal={true}
              isVerifying={false}
              onAdd={jest.fn()}
              onEdit={jest.fn()}
              onVerify={jest.fn()}
            />
          </Route>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    expect(
      screen.queryByText("group.toe.lines.actionButtons.verifyButton.text")
    ).toBeInTheDocument();
  });
});
