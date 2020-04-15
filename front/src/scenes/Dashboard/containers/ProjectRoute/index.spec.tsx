import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { configure, mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { MemoryRouter } from "react-router";
import { ProjectRoute, ProjectRouteProps } from "./index";
import { GET_PROJECT_ALERT, GET_PROJECT_DATA } from "./queries";

configure({ adapter: new ReactSixteenAdapter() });

describe("ProjectRoute", () => {

  const mockProps: ProjectRouteProps = {
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

  const projectMock: Readonly<MockedResponse> = {
    request: {
      query: GET_PROJECT_DATA,
      variables: {
        projectName: "TEST",
      },
    },
    result: {
      data: {
        project: {
          deletionDate: "",
          userDeletion: "",
        },
      },
    },
  };

  const alertMock: Readonly<MockedResponse> = {
    request: {
      query: GET_PROJECT_ALERT,
      variables: {
        organization: "Fluid",
        projectName: "TEST",
      },
    },
    result: {
      data: {
        alert: {
          message: "Hello world",
          status: 1,
        },
      },
    },
  };

  it("should return a function", () => {
    expect(typeof (ProjectRoute))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={[projectMock]} addTypename={false}>
        <ProjectRoute {...mockProps} />
      </MockedProvider>,
    );
    await act(async () => { await wait(0); });
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render alert", async () => {
    (window as typeof window & Dictionary<string>).userOrganization = "Fluid";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/indicators"]}>
        <MockedProvider mocks={[projectMock, alertMock]} addTypename={false}>
          <ProjectRoute {...mockProps} />
        </MockedProvider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("Hello world");
  });
});
