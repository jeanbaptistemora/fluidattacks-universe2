import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../../store/index";
import { authzPermissionsContext } from "../../../../../utils/authz/config";
import { msgError, msgSuccess } from "../../../../../utils/notifications";
import { ADD_ENVIRONMENTS_MUTATION, GET_ENVIRONMENTS, UPDATE_ENVIRONMENT_MUTATION } from "../queries";
import { Environments, IEnvironmentsProps } from "./index";

jest.mock("../../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../../utils/notifications");
  mockedNotifications.msgSuccess = jest.fn();
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

  const mocksEnvironments: ReadonlyArray<MockedResponse> = [
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
        <MockedProvider mocks={mocksEnvironments.concat(mocksMutation)} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Environments {...mockProps} />
          </authzPermissionsContext.Provider>
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

  it("should update an environment", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: UPDATE_ENVIRONMENT_MUTATION,
        variables: {
          env : {
            urlEnv: "https%3A%2F%2Ftest%2Ftest",
          },
          projectName: "TEST",
          state: "ACTIVE",
        },
      },
      result: { data: { updateEnvironment : { success: true } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_update_environment" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksEnvironments.concat(mocksMutation)} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Environments {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const stateSwitch: ReactWrapper = wrapper
      .find(".switch")
      .at(0);
    stateSwitch.simulate("click");
    const proceedButton: ReactWrapper = wrapper
      .find("button")
      .findWhere((element: ReactWrapper) => element.contains("Proceed"))
      .at(0);
    proceedButton.simulate("click");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgSuccess)
      .toHaveBeenCalled();
  });

  it("should sort environments", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksEnvironments} addTypename={false}>
          <Environments {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    let firstRowInfo: ReactWrapper = wrapper
      .find("RowPureContent")
      .at(0);
    expect(firstRowInfo.text())
      .toEqual("https://test/testInactive");
    const tagHeader: ReactWrapper = wrapper
      .find({"aria-label": "Environment sortable"});
    tagHeader.simulate("click");
    tagHeader.simulate("click");
    firstRowInfo = wrapper
      .find("RowPureContent")
      .at(0);
    expect(firstRowInfo.text())
      .toEqual("Docker image found at: https://test/testActive");
  });

  it("should filter environments by state", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksEnvironments} addTypename={false}>
          <Environments {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    let environmentRows: ReactWrapper = wrapper
      .find("SimpleRow");
    expect(environmentRows)
      .toHaveLength(2);
    const stateSelect: ReactWrapper = wrapper
      .find({id: "select-filter-column-state"});
    stateSelect.simulate("change", { target: { value: "Inactive" } });
    environmentRows = wrapper
      .find("SimpleRow");
    expect(environmentRows)
      .toHaveLength(1);
    expect(environmentRows.contains("Inactive"))
      .toEqual(true);
  });

  it("should handle errors when add an environment", async () => {
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
      result: { errors: [
        new GraphQLError("Access denied"),
        new GraphQLError("Exception - Invalid field in form"),
        new GraphQLError("Exception - One or more values already exist"),
        new GraphQLError("Exception - Invalid characters"),
      ]},
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_add_environments" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksEnvironments.concat(mocksMutation)} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Environments {...mockProps} />
          </authzPermissionsContext.Provider>
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
      .toBeCalledTimes(4);
  });
});
