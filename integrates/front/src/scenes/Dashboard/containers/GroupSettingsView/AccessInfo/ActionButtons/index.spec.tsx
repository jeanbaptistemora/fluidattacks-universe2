import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";

import { ActionButtons } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo/ActionButtons";
import type { IActionButtonsProps } from "scenes/Dashboard/containers/GroupSettingsView/AccessInfo/ActionButtons";
import { authzPermissionsContext } from "utils/authz/config";

describe("ActionButtons", (): void => {
  const baseMockedProps: IActionButtonsProps = {
    editTooltip: "tooltip",
    isEditing: false,
    isPristine: false,
    onEdit: jest.fn(),
    onUpdate: jest.fn(),
    permission: "api_mutations_update_group_access_info_mutate",
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toStrictEqual("function");
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_group_access_info_mutate" },
    ]);
    const { editTooltip, isEditing, isPristine, onEdit, onUpdate, permission } =
      baseMockedProps;
    const wrapper: ReactWrapper = mount(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons
          editTooltip={editTooltip}
          isEditing={isEditing}
          isPristine={isPristine}
          onEdit={onEdit}
          onUpdate={onUpdate}
          permission={permission}
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
