import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../../store/index";
import { authzContext } from "../../../../../utils/authz/config";
import { msgError } from "../../../../../utils/notifications";
import { ADD_ENVIRONMENTS_MUTATION, GET_ENVIRONMENTS } from "../queries";
import { Environments, IEnvironmentsProps } from "./index";

jest.mock("../../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();

  return mockedNotifications;
});

describe("Environments", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  const mockProps: IEnvironmentsProps = {
    projectName: "TEST",
  };

  const mocksRepositories: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_ENVIRONMENTS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          resources: {
            environments: JSON.stringify([
              {
                historic_state: [{
                  date: "2000/03/24 15:43:48",
                  state: "INACTIVE",
                  user: "test@gmail.com",
                }],
                urlEnv: "https://test/test",
              },
              {
                historic_state: [{
                  date: "2000/03/24 15:45:00",
                  state: "ACTIVE",
                  user: "test@gmail.com",
                }],
                urlEnv: "Docker image found at: https://test/test",
              },
            ]),
          },
        },
      },
    },
    {
      request: {
        query: GET_ENVIRONMENTS,
        variables: {
          addEnvironments : { success: true },
          projectName: "TEST",
        },
      },
      result: {
        data: {
          resources: {
            environments: JSON.stringify([
              {
                historic_state: [{
                  date: "2000/03/24 15:43:48",
                  state: "INACTIVE",
                  user: "test@gmail.com",
                }],
                urlEnv: "https://test/test",
              },
              {
                historic_state: [{
                  date: "2000/03/24 15:45:00",
                  state: "ACTIVE",
                  user: "test@gmail.com",
                }],
                urlEnv: "Docker image found at: https://test/test",
              },
            ]),
          },
        },
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof (Environments))
      .toEqual("function");
  });

  it("should add an environment", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: ADD_ENVIRONMENTS_MUTATION,
        variables: {
          envs: [{
            urlEnv: "test-new-environment",
          }],
          projectName: "TEST",
        },
      },
      result: { data: { addEnvironments : { success: true } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_add_environments" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksRepositories.concat(mocksMutation)} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <Environments {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addEnvironmentsModal: ReactWrapper = wrapper.find("addEnvironmentsModal");
    const environmentInput: ReactWrapper = addEnvironmentsModal
      .find({name: "resources[0].urlEnv", type: "text"})
      .at(0)
      .find("textarea");
    environmentInput.simulate("change", { target: { value: "test-new-environment" } });
    const form: ReactWrapper = addEnvironmentsModal
      .find("genericForm")
      .at(0);
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgError)
      .toHaveBeenCalledTimes(0);
  });
});
