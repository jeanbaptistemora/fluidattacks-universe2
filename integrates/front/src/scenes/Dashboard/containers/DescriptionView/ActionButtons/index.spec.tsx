import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { ActionButtons, IActionButtonsProps } from "scenes/Dashboard/containers/DescriptionView/ActionButtons";
import { authzPermissionsContext } from "utils/authz/config";

describe("ActionButtons", () => {

  const baseMockedProps: IActionButtonsProps = {
    isEditing: false,
    isPristine: false,
    lastTreatment: {
      acceptanceDate: "",
      acceptanceStatus: "",
      date: "",
      justification: "",
      treatment: "",
      user: "",
    },
    onApproveAcceptation: jest.fn(),
    onEdit: jest.fn(),
    onRejectAcceptation: jest.fn(),
    onUpdate: jest.fn(),
    state: "open",
  };

  it("should return a function", () => {
    expect(typeof (ActionButtons))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_finding__do_update_description" },
    ]);
    const wrapper: ReactWrapper = mount(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons {...baseMockedProps} />
      </authzPermissionsContext.Provider>,
    );
    expect(wrapper)
      .toHaveLength(1);
    const buttons: ReactWrapper = wrapper.find("Button");
    expect(buttons)
      .toHaveLength(1);
    expect(buttons
      .filterWhere((button: ReactWrapper): boolean =>
        button
          .text()
          .includes("Edit")))
      .toHaveLength(1);
  });

});
