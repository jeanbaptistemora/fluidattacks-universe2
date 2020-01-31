import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { MockedProvider, MockedResponse } from "react-apollo/test-utils";
import { Provider } from "react-redux";
import store from "../../../../store";
import { RemoveProjectModal } from "./index";
import { REQUEST_REMOVE_PROJECT_MUTATION } from "./queries";
import { IRemoveProject } from "./types";

configure({ adapter: new ReactSixteenAdapter() });

describe("RemoveProjectModal component", () => {
  it("should render remove project modal", () => {
    const handleOnClose: jest.Mock = jest.fn();
    const projectName: IRemoveProject = {
      requestRemoveProject: {
        success: true,
      },
    };
    const mocksMutation: MockedResponse[] = [{
        request: {
          query: REQUEST_REMOVE_PROJECT_MUTATION,
        },
        result: {
          data: { projectName },
        },
      }];
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksMutation} addTypename={false}>
          <RemoveProjectModal
            isOpen={true}
            onClose={handleOnClose}
            projectName={""}
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
