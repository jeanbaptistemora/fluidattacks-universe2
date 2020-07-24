import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import store from "../../../../store";
import { AddProjectModal } from "./index";
import { PROJECTS_NAME_QUERY } from "./queries";
import { IProjectName } from "./types";

describe("AddProjectModal component", () => {

  const projectName: IProjectName = { internalProjectNames : { projectName: "" } };

  const mocksMutation: MockedResponse[] = [{
    request: {
      query: PROJECTS_NAME_QUERY,
    },
    result: {
      data: { projectName },
    },
  }];

  const handleOnClose: jest.Mock = jest.fn();

  it("should render add project modal", () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <AddProjectModal
            isOpen={true}
            onClose={handleOnClose}
            organization="testorg"
          />
        </MockedProvider>
      </Provider>,
    );

    const cancelButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.contains("Cancel"));
    cancelButton.simulate("click");
    expect(wrapper)
      .toHaveLength(1);
    expect(handleOnClose.mock.calls.length)
      .toEqual(1);
  });

  it("should render form fields", () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <AddProjectModal
            isOpen={true}
            onClose={handleOnClose}
            organization="testorg"
          />
        </MockedProvider>
      </Provider>,
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

    const switchButtons: ReactWrapper = wrapper
      .find({ checked: true })
      .find(".switch-group");

    const submitButton: ReactWrapper = wrapper
    .findWhere((element: ReactWrapper) => element.contains("Proceed"))
    .at(0);

    expect(organizationField)
      .toHaveLength(1);
    expect(projectNameField)
      .toHaveLength(1);
    expect(descriptionField)
      .toHaveLength(1);
    expect(typeField)
      .toHaveLength(1);
    expect(switchButtons)
      .toHaveLength(3);
    expect(submitButton)
      .toHaveLength(1);

  });

  it("should remove Forces and Drills switches", () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <AddProjectModal
            isOpen={true}
            onClose={handleOnClose}
            organization="testorg"
          />
        </MockedProvider>
      </Provider>,
    );

    wrapper
      .find({ name: "type" })
      .find("select")
      .simulate("change", { target: { value: "ONESHOT" } });

    expect(wrapper.find({ checked: true })
      .find(".switch-group"))
      .toHaveLength(2);
  });

  it("should remove Forces Service switch", () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <AddProjectModal
            isOpen={true}
            onClose={handleOnClose}
            organization="testorg"
          />
        </MockedProvider>
      </Provider>,
    );

    const drillsSwitch: ReactWrapper = wrapper
      .find({ checked: true })
      .find(".switch-group")
      .at(1);

    drillsSwitch
      .simulate("click");

    expect(wrapper
      .find({ checked: true })
      .find(".switch-group"))
      .toHaveLength(1);
  });
});
