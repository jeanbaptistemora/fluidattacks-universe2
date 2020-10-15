import { AddProjectModal } from "scenes/Dashboard/components/AddProjectModal";
import { IProjectNameProps } from "scenes/Dashboard/components/AddProjectModal/types";
import { PROJECTS_NAME_QUERY } from "scenes/Dashboard/components/AddProjectModal/queries";
import { Provider } from "react-redux";
import React from "react";
import store from "store";
import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { ReactWrapper, mount } from "enzyme";

describe("AddProjectModal component", (): void => {
  const projectName: IProjectNameProps = { internalNames: { name: "" } };

  const mocksMutation: MockedResponse[] = [
    {
      request: {
        query: PROJECTS_NAME_QUERY,
      },
      result: {
        data: { projectName },
      },
    },
  ];

  const handleOnClose: jest.Mock = jest.fn();

  it("should render add project modal", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <AddProjectModal
            isOpen={true}
            onClose={handleOnClose}
            organization={"okada"}
          />
        </MockedProvider>
      </Provider>
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
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <AddProjectModal
            isOpen={true}
            onClose={handleOnClose}
            organization={"okada"}
          />
        </MockedProvider>
      </Provider>
    );

    const organizationField: ReactWrapper = wrapper
      .find({ name: "organization" })
      .find("input");

    const projectNameField: ReactWrapper = wrapper
      .find({ name: "name" })
      .find("input");

    const descriptionField: ReactWrapper = wrapper
      .find({ name: "description" })
      .find("input");

    const typeField: ReactWrapper = wrapper
      .find({ name: "type" })
      .find("select");

    const switchButtons: ReactWrapper = wrapper.find({ checked: true });

    const submitButton: ReactWrapper = wrapper
      .findWhere((element: ReactWrapper): boolean =>
        element.contains("Proceed")
      )
      .at(0);
    const SWITCH_BUTTON_LENGTH: number = 3;

    expect(organizationField).toHaveLength(1);
    expect(projectNameField).toHaveLength(1);
    expect(descriptionField).toHaveLength(1);
    expect(typeField).toHaveLength(1);
    expect(switchButtons).toHaveLength(SWITCH_BUTTON_LENGTH);
    expect(submitButton).toHaveLength(1);
  });

  it("should remove Forces and Drills switches", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <AddProjectModal
            isOpen={true}
            onClose={handleOnClose}
            organization={"okada"}
          />
        </MockedProvider>
      </Provider>
    );

    wrapper
      .find({ name: "type" })
      .find("select")
      .simulate("change", { target: { value: "ONESHOT" } });

    expect(wrapper.find({ checked: true })).toHaveLength(2);
  });

  it("should remove Forces Service switch", (): void => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mocksMutation}>
          <AddProjectModal
            isOpen={true}
            onClose={handleOnClose}
            organization={"okada"}
          />
        </MockedProvider>
      </Provider>
    );

    const drillsSwitch: ReactWrapper = wrapper.find({ checked: true }).at(1);

    drillsSwitch.simulate("click");

    expect(wrapper.find({ checked: true })).toHaveLength(1);
  });
});
