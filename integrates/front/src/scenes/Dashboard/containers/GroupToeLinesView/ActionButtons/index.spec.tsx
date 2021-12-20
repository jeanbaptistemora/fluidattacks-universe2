import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { useTranslation } from "react-i18next";

import { ActionButtons } from ".";
import { authzPermissionsContext } from "utils/authz/config";

describe("ToelinesActionButtons", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toStrictEqual("function");
  });

  it("should not display the edition button without permissions", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <ActionButtons isEditing={false} isInternal={true} onEdit={jest.fn()} />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: new PureAbility([]) },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(0);
  });

  it("should hide the edition button for the external view", (): void => {
    expect.hasAssertions();

    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_toe_lines_attacked_lines_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons isEditing={false} isInternal={false} onEdit={jest.fn()} />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(0);
  });

  it("should display the edition button", (): void => {
    expect.hasAssertions();

    const { t } = useTranslation();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_update_toe_lines_attacked_lines_mutate" },
    ]);
    const wrapper: ReactWrapper = mount(
      <ActionButtons isEditing={false} isInternal={true} onEdit={jest.fn()} />,
      {
        wrappingComponent: authzPermissionsContext.Provider,
        wrappingComponentProps: { value: mockedPermissions },
      }
    );
    const buttons: ReactWrapper = wrapper.find("Button");

    expect(wrapper).toHaveLength(1);
    expect(buttons).toHaveLength(1);
    expect(
      buttons.filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes(t("group.toe.lines.actionButtons.editButton.text"))
      )
    ).toHaveLength(1);
  });
});
