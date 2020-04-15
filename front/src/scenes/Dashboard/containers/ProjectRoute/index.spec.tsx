import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { ProjectRoute, ProjectRouteProps } from "./index";
import { GET_PROJECT_DATA } from "./queries";

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
});
