import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../store/index";
import { ProjectIndicatorsView } from "./index";
import { GET_INDICATORS } from "./queries";
import { IIndicatorsViewBaseProps } from "./types";

describe("ProjectIndicatorsView", () => {

  const mockProps: IIndicatorsViewBaseProps = {
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
            deletionDate: "",
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
            userDeletion: "",
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

  it("should return an function", () => {
    expect(typeof (ProjectIndicatorsView))
      .toEqual("function");
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={true}>
          <ProjectIndicatorsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mocks} addTypename={true}>
          <ProjectIndicatorsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });
});
