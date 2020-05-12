import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import wait from "waait";
import store from "../../../../store";
import { PROJECTS_QUERY } from "../../containers/HomeView/queries";
import { RemoveProjectModal } from "./index";
import { REQUEST_REMOVE_PROJECT_MUTATION } from "./queries";
import { IRemoveProject } from "./types";

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
      <MemoryRouter initialEntries={["/project/test/resources"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocksMutation} addTypename={false}>
            <RemoveProjectModal
              isOpen={true}
              onClose={handleOnClose}
              projectName={""}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    const inputField: ReactWrapper = wrapper
      .find("input");
    const cancelButton: ReactWrapper = wrapper
      .find("Button")
      .filterWhere((element: ReactWrapper) => element.contains("Cancel"));

    expect(inputField)
      .toHaveLength(1);
    cancelButton.simulate("click");
    expect(wrapper)
      .toHaveLength(1);
    expect(handleOnClose.mock.calls.length)
      .toEqual(1);
  });

  it("should render project modal and submit", async () => {
    const handleOnClose: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REQUEST_REMOVE_PROJECT_MUTATION,
          variables: {projectName: "test"},
        },
        result: jest.fn(() => ({
          data: { requestRemoveProject: { success: true }},
        })),
      },
      {
        request: {
          query: PROJECTS_QUERY,
          variables: { tagsField: false },
        },
        result: {
          data: { me: { projects: [] }},
        },
      }];
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/test/resources"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocksMutation} addTypename={false}>
            <RemoveProjectModal
              isOpen={true}
              onClose={handleOnClose}
              projectName={"test"}
            />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    const projectName: ReactWrapper = wrapper.find("input[value=\"\"]");
    projectName.simulate("change", { target: { value: "test" } });
    const form: ReactWrapper = wrapper.find("genericForm");
    form.simulate("submit");
    const { result }: MockedResponse = mocksMutation[0];

    await act(async () => { await wait(0); expect(result)
      .toHaveBeenCalled(); });
    expect(wrapper)
      .toHaveLength(1);
  });
});
