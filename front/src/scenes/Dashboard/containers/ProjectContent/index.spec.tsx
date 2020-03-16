import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import * as React from "react";
import { Provider } from "react-redux";
import { MemoryRouter, RouteComponentProps } from "react-router-dom";
import wait from "waait";
import store from "../../../../store/index";
import { GET_INDICATORS } from "../IndicatorsView/queries";
import { ProjectContent } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("ProjectContent", () => {

  const mockProps: RouteComponentProps<{ projectName: string }> = {
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
      params: {projectName: "TEST"},
      path: "/",
      url: "",
    },
  };

  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_INDICATORS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        data: {
          project: {
            __typename: "Project",
            closedVulnerabilities: 29,
            currentMonthAuthors: 0,
            currentMonthCommits: 0,
            lastClosingVuln: 33,
            maxOpenSeverity: 10,
            maxSeverity: 10,
            meanRemediate: 53,
            openVulnerabilities: 27,
            pendingClosingCheck: 0,
            remediatedOverTime: JSON.stringify([
              [{y: 2, x: "Jun 10 - 16, 2019"}, {y: 12, x: "Jun 17 - 23, 2019"}],
              [{y: 0, x: "Jun 10 - 16, 2019"}, {y: 0, x: "Jun 17 - 23, 2019"}],
              [{y: 0, x: "Jun 10 - 16, 2019"}, {y: 0, x: "Jun 17 - 23, 2019"}],
              [{y: 0, x: "Jun 10 - 16, 2019"}, {y: 0, x: "Jun 17 - 23, 2019"}]]),
            totalFindings: 4,
            totalTreatment: "{\"inProgress\": 6, \"accepted\": 0, \"undefined\": 21}",
          },
          resources: {
            __typename: "Resource",
            repositories: "[{\"urlRepo\": \"https://gitlab.com/test\", \"branch\": \"master\"}]",
          },
        },
      },
  }];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_INDICATORS,
        variables: {
          projectName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
  }];

  it("should return a function", () => {
    expect(typeof (ProjectContent))
      .toEqual("function");
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/indicators"]}>
        <Provider store={store}>
          <MockedProvider mocks={mockError} addTypename={true}>
            <ProjectContent {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/indicators"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={true}>
            <ProjectContent {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });
});
