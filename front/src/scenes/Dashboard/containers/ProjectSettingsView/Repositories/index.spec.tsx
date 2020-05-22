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
import { authzContext } from "../../../../../utils/authz/config";
import { msgError, msgSuccess } from "../../../../../utils/notifications";
import { ADD_REPOSITORIES_MUTATION, GET_REPOSITORIES, UPDATE_REPOSITORY_MUTATION } from "../queries";
import { IRepositoriesProps, Repositories } from "./index";

jest.mock("../../../../../utils/notifications", () => {
  const mockedNotifications: Dictionary = jest.requireActual("../../../../../utils/notifications");
  mockedNotifications.msgError = jest.fn();
  mockedNotifications.msgSuccess = jest.fn();

  return mockedNotifications;
});

describe("Repositories", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  const mockProps: IRepositoriesProps = {
    projectName: "TEST",
  };

  const mocksRepositories: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_REPOSITORIES,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          resources: {
            repositories: JSON.stringify([
              {
                branch: "develop",
                historic_state: [
                  {
                    date: "2020/02/13 10:15:26",
                    state: "ACTIVE",
                    user: "test@gmail.com",
                  },
                  {
                    date: "2020/03/24 09:16:15",
                    state: "INACTIVE",
                    user: "test@gmail.com",
                  },
                ],
                protocol: "HTTPS",
                uploadDate: "2020-02-13 10:15",
                urlRepo: "pruebarepo/git",
              },
              {
                branch: "master",
                historic_state: [
                  {
                    date: "2020/02/13 10:15:26",
                    state: "ACTIVE",
                    user: "test@gmail.com",
                  },
                  {
                    date: "2020/03/24 09:16:19",
                    state: "ACTIVE",
                    user: "test@gmail.com",
                  },
                ],
                protocol: "SSH",
                uploadDate: "2020-02-13 10:15",
                urlRepo: "pruebarepo/git2",
              },
            ]),
          },
        },
      },
    },
    {
      request: {
        query: GET_REPOSITORIES,
        variables: {
          addRepositories : {
            success: true,
          },
          projectName : "TEST",
        },
      },
      result: {
        data: {
          resources: {
            repositories: JSON.stringify([
              {
                branch: "develop",
                historic_state: [
                  {
                    date: "2020/02/13 10:15:26",
                    state: "ACTIVE",
                    user: "test@gmail.com",
                  },
                  {
                    date: "2020/03/24 09:16:15",
                    state: "ACTIVE",
                    user: "test@gmail.com",
                  },
                ],
                protocol: "HTTPS",
                uploadDate: "2020-02-13 10:15",
                urlRepo: "pruebarepo/git",
              },
            ]),
          },
        },
      },
    },
    {
      request: {
        query: GET_REPOSITORIES,
        variables: {
          projectName : "TEST",
        },
      },
      result: {
        data: {
          resources: {
            repositories: JSON.stringify([
              {
                branch: "develop",
                historic_state: [
                  {
                    date: "2020/02/13 10:15:26",
                    state: "ACTIVE",
                    user: "test@gmail.com",
                  },
                  {
                    date: "2020/03/24 09:16:15",
                    state: "ACTIVE",
                    user: "test@gmail.com",
                  },
                ],
                protocol: "HTTPS",
                uploadDate: "2020-02-13 10:15",
                urlRepo: "pruebarepo/git",
              },
            ]),
          },
        },
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof (Repositories))
      .toEqual("function");
  });

  it("should add a repository", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: ADD_REPOSITORIES_MUTATION,
        variables: {
          projectName: "TEST",
          repos: [
            {
              branch: "master",
              protocol : "HTTPS",
              urlRepo: "gitlab.com/test/test.git",
            },
          ],
        },
      },
      result: { data: { addRepositories : { success: true } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_add_repositories" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksRepositories.concat(mocksMutation)} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <Repositories {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addRepositoriesModal: ReactWrapper = wrapper.find("addRepositoriesModal");
    const repositoryInput: ReactWrapper = addRepositoriesModal
    .find({name: "resources[0].urlRepo", type: "text"})
    .at(0)
    .find("input");
    repositoryInput.simulate("change", { target: { value: "gitlab.com/test/test.git" } });
    const protocolSelect: ReactWrapper = addRepositoriesModal
      .find("select")
      .findWhere((element: ReactWrapper) => element.contains("HTTPS"))
      .at(0);
    protocolSelect.simulate("change", { target: { value: "HTTPS" } });
    const branchInput: ReactWrapper = addRepositoriesModal
    .find({name: "resources[0].branch", type: "text"})
    .at(0)
    .find("input");
    branchInput.simulate("change", { target: { value: "master" } });
    const form: ReactWrapper = addRepositoriesModal
      .find("genericForm")
      .at(0);
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgError)
      .toHaveBeenCalledTimes(0);
  });

  it("should update a repository", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: UPDATE_REPOSITORY_MUTATION,
        variables: {
          projectName: "TEST",
          repo: {
            branch: "develop",
            protocol: "HTTPS",
            urlRepo: "pruebarepo/git",
          },
          state: "ACTIVE",
        },
      },
      result: { data: { updateRepository : { success: true } } },
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_update_repository" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksRepositories.concat(mocksMutation)} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <Repositories {...mockProps} />
          </authzContext.Provider>
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

  it("should sort repositories", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksRepositories} addTypename={false}>
          <Repositories {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    let firstRowInfo: ReactWrapper = wrapper
      .find("RowPureContent")
      .at(0);
    expect(firstRowInfo.text())
      .toEqual("HTTPSpruebarepo/gitdevelopInactive");
    const repositoryHeader: ReactWrapper = wrapper
      .find({"aria-label": "Protocol sortable"});
    repositoryHeader.simulate("click");
    firstRowInfo = wrapper
      .find("RowPureContent")
      .at(0);
    expect(firstRowInfo.text())
      .toEqual("SSHpruebarepo/git2masterActive");
  });

  it("should handle errors when add a repository", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: ADD_REPOSITORIES_MUTATION,
        variables: {
          projectName: "TEST",
          repos: [
            {
              branch: "master",
              protocol : "HTTPS",
              urlRepo: "gitlab.com/test/test.git",
            },
          ],
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
      { action: "backend_api_resolvers_resource__do_add_repositories" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksRepositories.concat(mocksMutation)} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <Repositories {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addRepositoriesModal: ReactWrapper = wrapper.find("addRepositoriesModal");
    const repositoryInput: ReactWrapper = addRepositoriesModal
    .find({name: "resources[0].urlRepo", type: "text"})
    .at(0)
    .find("input");
    repositoryInput.simulate("change", { target: { value: "gitlab.com/test/test.git" } });
    const protocolSelect: ReactWrapper = addRepositoriesModal
      .find("select")
      .findWhere((element: ReactWrapper) => element.contains("HTTPS"))
      .at(0);
    protocolSelect.simulate("change", { target: { value: "HTTPS" } });
    const branchInput: ReactWrapper = addRepositoriesModal
    .find({name: "resources[0].branch", type: "text"})
    .at(0)
    .find("input");
    branchInput.simulate("change", { target: { value: "master" } });
    const form: ReactWrapper = addRepositoriesModal
      .find("genericForm")
      .at(0);
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgError)
      .toHaveBeenCalledTimes(4);
  });

  it("should handle error when update a repository", async () => {
    const mocksMutation: ReadonlyArray<MockedResponse> = [{
      request: {
        query: UPDATE_REPOSITORY_MUTATION,
        variables: {
          projectName: "TEST",
          repo: {
            branch: "develop",
            protocol: "HTTPS",
            urlRepo: "pruebarepo/git",
          },
          state: "ACTIVE",
        },
      },
      result: { errors: [
        new GraphQLError("Access denied"),
      ]},
    }];
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_update_repository" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksRepositories.concat(mocksMutation)} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <Repositories {...mockProps} />
          </authzContext.Provider>
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
    expect(msgError)
      .toHaveBeenCalled();
  });

  it("should handle error when there are repeated repositories", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_add_repositories" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocksRepositories} addTypename={false}>
          <authzContext.Provider value={mockedPermissions}>
            <Repositories {...mockProps} />
          </authzContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    const addButton: ReactWrapper = wrapper.find("button")
      .findWhere((element: ReactWrapper) => element.contains("Add"))
      .at(0);
    addButton.simulate("click");
    const addRepositoriesModal: ReactWrapper = wrapper.find("addRepositoriesModal");
    const repositoryInput: ReactWrapper = addRepositoriesModal
    .find({name: "resources[0].urlRepo", type: "text"})
    .at(0)
    .find("input");
    repositoryInput.simulate("change", { target: { value: "pruebarepo/git" } });
    const protocolSelect: ReactWrapper = addRepositoriesModal
      .find("select")
      .findWhere((element: ReactWrapper) => element.contains("HTTPS"))
      .at(0);
    protocolSelect.simulate("change", { target: { value: "HTTPS" } });
    const branchInput: ReactWrapper = addRepositoriesModal
    .find({name: "resources[0].branch", type: "text"})
    .at(0)
    .find("input");
    branchInput.simulate("change", { target: { value: "develop" } });
    const form: ReactWrapper = addRepositoriesModal
      .find("genericForm")
      .at(0);
    form.simulate("submit");
    await act(async () => { await wait(0); wrapper.update(); });
    expect(msgError)
      .toHaveBeenCalled();
  });
});
