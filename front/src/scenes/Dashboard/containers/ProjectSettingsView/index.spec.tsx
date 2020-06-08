import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../store/index";
import { authzPermissionsContext } from "../../../../utils/authz/config";
import { ProjectSettingsView } from "./index";
import { GET_ENVIRONMENTS, GET_REPOSITORIES, GET_TAGS } from "./queries";
import { ISettingsViewProps } from "./types";

describe("ProjectSettingsView", () => {

  const mockProps: ISettingsViewProps = {
    history: {
      action: "PUSH",
      block: (): (() => void) => (): void => undefined,
      createHref: (): string => "",
      go: (): void => undefined,
      goBack: (): void => undefined,
      goForward: (): void => undefined,
      length: 1,
      listen: (): (() => void) => (): void => undefined,
      location: { hash: "", pathname: "/", search: "", state: {} },
      push: (): void => undefined,
      replace: (): void => undefined,
    },
    location: { hash: "", pathname: "/", search: "", state: {} },
    match: {
      isExact: true,
      params: { projectName: "TEST" },
      path: "/",
      url: "",
    },
  };

  const mocksTags: Readonly<MockedResponse> = {
      request: {
        query: GET_TAGS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            tags: ["test"],
          },
        },
      },
  };

  const mocksRepositories: Readonly<MockedResponse> = {
      request: {
        query: GET_REPOSITORIES,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          resources: {
            repositories: JSON.stringify([{
              branch: "test",
              historic_state: [{ state: "ACTIVE" }],
              protocol: "HTTPS",
              urlRepo: "https://gitlab.com/fluidattacks/integrates",
            }]),
          },
        },
      },
  };

  const mocksEnvironments: Readonly<MockedResponse> = {
      request: {
        query: GET_ENVIRONMENTS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          resources: {
            environments: JSON.stringify([{
              urlEnv: "https://gitlab.com/fluidattacks/integrates",
            }]),
          },
        },
      },
  };

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_TAGS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", () => {
    expect(typeof (ProjectSettingsView))
      .toEqual("function");
  });

  it("should render tags component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[mocksTags]} addTypename={false}>
          <ProjectSettingsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render repositories component", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_update_repository" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[mocksRepositories]} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <ProjectSettingsView {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(500); wrapper.update(); });
    const onerow: ReactWrapper = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell");
    const statuschecked: boolean | undefined = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell")
      .at(3)
      .find("e")
      .prop("checked");
    const protocol: string = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell")
      .at(0)
      .find("td")
      .text();
    expect(wrapper)
      .toHaveLength(1);
    expect(onerow)
      .toHaveLength(4);
    expect(statuschecked)
      .toEqual(true || false);
    expect(protocol)
      .toMatch(/^(HTTPS|SSH)$/);
  });

  it("should render environments component", async () => {
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "backend_api_resolvers_resource__do_update_environment" },
    ]);
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[mocksEnvironments]} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <ProjectSettingsView {...mockProps} />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(200); wrapper.update(); });
    const onerow: ReactWrapper = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell");
    const statuschecked: boolean | undefined = wrapper
      .find("BootstrapTable")
      .find("RowPureContent")
      .find("Cell")
      .at(1)
      .find("e")
      .prop("checked");
    expect(wrapper)
      .toHaveLength(1);
    expect(onerow)
      .toHaveLength(2);
    expect(statuschecked)
      .toEqual(true || false);
  });

  it("should render a error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={false}>
          <ProjectSettingsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render files component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[mocksTags]} addTypename={false}>
          <ProjectSettingsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper.find("#tblFiles"))
      .toBeTruthy();
  });
});
