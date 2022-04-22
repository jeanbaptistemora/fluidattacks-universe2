import { PureAbility } from "@casl/ability";
import { render, screen } from "@testing-library/react";
import React from "react";

import { ActionButtons } from "scenes/Dashboard/containers/DescriptionView/ActionButtons";
import type { IActionButtonsProps } from "scenes/Dashboard/containers/DescriptionView/ActionButtons";
import { authzPermissionsContext } from "utils/authz/config";

describe("ActionButtons", (): void => {
  const baseMockedProps: IActionButtonsProps = {
    isEditing: false,
    isPristine: false,
    onEdit: jest.fn(),
    onUpdate: jest.fn(),
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toBe("function");
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_finding_description_mutate" },
    ]);
    const { isEditing, isPristine, onEdit, onUpdate } = baseMockedProps;
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons
          isEditing={isEditing}
          isPristine={isPristine}
          onEdit={onEdit}
          onUpdate={onUpdate}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabDescription.editable.text")
    ).toBeInTheDocument();
  });
});
