import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { useTranslation } from "react-i18next";

import { ActionButtons } from ".";
import { authzPermissionsContext } from "utils/authz/config";

describe("ToeInputsActionButtons", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toStrictEqual("function");
  });

  it("should not display the edition button without permissions", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areInputsSelected={true}
        isAdding={false}
        isEditing={false}
        isInternal={true}
        onAdd={jest.fn()}
        onEdit={jest.fn()}
      />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: new PureAbility([]) },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(0);
  });

  it("should hide the addition button for the external view", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_toe_input_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areInputsSelected={true}
        isAdding={false}
        isEditing={false}
        isInternal={false}
        onAdd={jest.fn()}
        onEdit={jest.fn()}
      />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(0);
  });

  it("should display the addition button", (): void => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_toe_input_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areInputsSelected={true}
        isAdding={false}
        isEditing={false}
        isInternal={true}
        onAdd={jest.fn()}
        onEdit={jest.fn()}
      />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper).toHaveLength(1);
    expect(
      buttons.filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("group.toe.inputs.actionButtons.addButton.text"))
      )
    ).toHaveLength(1);
  });

  it("should display the edition button", (): void => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_toe_input_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons
        areInputsSelected={true}
        isAdding={false}
        isEditing={false}
        isInternal={true}
        onAdd={jest.fn()}
        onEdit={jest.fn()}
      />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper).toHaveLength(1);
    expect(
      buttons.filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("group.toe.inputs.actionButtons.editButton.text"))
      )
    ).toHaveLength(1);
  });
});
