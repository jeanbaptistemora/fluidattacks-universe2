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
          />
        </MockedProvider>
      </Provider>,
    );

    const companyField: ReactWrapper = wrapper
      .find({ name: "company" })
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

    expect(companyField)
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
});
