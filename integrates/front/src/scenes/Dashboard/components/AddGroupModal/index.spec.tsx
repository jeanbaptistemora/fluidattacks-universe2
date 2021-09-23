import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";

import { AddGroupModal } from "scenes/Dashboard/components/AddGroupModal";
import { GROUPS_NAME_QUERY } from "scenes/Dashboard/components/AddGroupModal/queries";
import type { IGroupNameProps } from "scenes/Dashboard/components/AddGroupModal/types";

describe("AddGroupModal component", (): void => {
  const groupName: IGroupNameProps = { internalNames: { name: "" } };

  const mocksMutation: MockedResponse[] = [
    {
      request: {
        query: GROUPS_NAME_QUERY,
      },
      result: {
        data: { groupName },
      },
    },
  ];

  const handleOnClose: jest.Mock = jest.fn();

  it("should render add group modal", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mocksMutation}>
        <AddGroupModal
          isOpen={true}
          onClose={handleOnClose}
          organization={"okada"}
        />
      </MockedProvider>
    );

    const cancelButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((element: ReactWrapper): boolean =>
        element.contains("Cancel")
      );
    cancelButton.simulate("click");

    expect(wrapper).toHaveLength(1);
    expect(handleOnClose.mock.calls).toHaveLength(1);
  });

  it("should render form fields", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <MockedProvider addTypename={false} mocks={mocksMutation}>
        <AddGroupModal
          isOpen={true}
          onClose={handleOnClose}
          organization={"okada"}
        />
      </MockedProvider>
    );

    const organizationField: ReactWrapper = wrapper
      .find({ name: "organization" })
      .find("input");

    const groupNameField: ReactWrapper = wrapper
      .find({ name: "name" })
      .find("input");

    const descriptionField: ReactWrapper = wrapper
      .find({ name: "description" })
      .find("input");

    const typeField: ReactWrapper = wrapper
      .find({ name: "type" })
      .find("select");

    const serviceField: ReactWrapper = wrapper
      .find({ name: "service" })
      .find("select");

    const switchButtons: ReactWrapper = wrapper.find({ checked: true });

    const submitButton: ReactWrapper = wrapper
      .findWhere((element: ReactWrapper): boolean =>
        element.contains("Proceed")
      )
      .at(0);

    expect(organizationField).toHaveLength(1);
    expect(groupNameField).toHaveLength(1);
    expect(descriptionField).toHaveLength(1);
    expect(typeField).toHaveLength(1);
    expect(serviceField).toHaveLength(1);
    expect(switchButtons).toHaveLength(2);
    expect(submitButton).toHaveLength(1);
  });
});
