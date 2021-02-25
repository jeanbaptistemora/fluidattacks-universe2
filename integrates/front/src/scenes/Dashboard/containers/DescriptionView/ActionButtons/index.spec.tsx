import { ActionButtons } from "scenes/Dashboard/containers/DescriptionView/ActionButtons";
import type { IActionButtonsProps } from "scenes/Dashboard/containers/DescriptionView/ActionButtons";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { authzPermissionsContext } from "utils/authz/config";
import { mount } from "enzyme";

describe("ActionButtons", (): void => {
  const baseMockedProps: IActionButtonsProps = {
    isEditing: false,
    isPristine: false,
    onEdit: jest.fn(),
    onUpdate: jest.fn(),
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toStrictEqual("function");
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_mutations_update_finding_description_mutate" },
    ]);
    const { isEditing, isPristine, onEdit, onUpdate } = baseMockedProps;
    const wrapper: ReactWrapper = mount(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons
          isEditing={isEditing}
          isPristine={isPristine}
          onEdit={onEdit}
          onUpdate={onUpdate}
        />
      </authzPermissionsContext.Provider>
    );

    expect(wrapper).toHaveLength(1);

    const buttons: ReactWrapper = wrapper.find("Button");

    expect(buttons).toHaveLength(1);
    expect(
      buttons.filterWhere((button: ReactWrapper): boolean =>
        button.text().includes("Edit")
      )
    ).toHaveLength(1);
  });
});
