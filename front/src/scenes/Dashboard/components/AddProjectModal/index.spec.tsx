import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import store from "../../../../store";
import { AddProjectModal } from "./index";
import { PROJECTS_NAME_QUERY } from "./queries";
import { IProjectName } from "./types";

describe("AddProjectModal component", () => {
  it("should render add project modal", () => {
    const handleOnClose: jest.Mock = jest.fn();
    const projectName: IProjectName = { internalProjectNames : { projectName: "" } };
    const mocksMutation: MockedResponse[] = [{
        request: {
          query: PROJECTS_NAME_QUERY,
        },
        result: {
          data: { projectName },
        },
      }];
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
});
