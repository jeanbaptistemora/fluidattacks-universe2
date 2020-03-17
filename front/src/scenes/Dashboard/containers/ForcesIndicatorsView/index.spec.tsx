import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import * as React from "react";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../store/index";
import { ForcesIndicatorsView } from "./index";
import { GET_INDICATORS } from "./queries";
import { IForcesIndicatorsViewBaseProps } from "./types";

configure({ adapter: new ReactSixteenAdapter() });

describe("ForcesIndicatorsView", () => {

  const mockProps: IForcesIndicatorsViewBaseProps = { projectName: "TEST" };

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
          forcesExecutions: {
            executions: [
              {
                strictness: "strict",
                vulnerabilities: {
                  numOfVulnerabilitiesInAcceptedExploits: 1,
                  numOfVulnerabilitiesInExploits: 2,
                  numOfVulnerabilitiesInMockedExploits: 3,
                },
              },
            ],
          },
          project: {
            hasForces: true,
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
    expect(typeof (ForcesIndicatorsView))
      .toEqual("function");
  });

  it("should render an error in component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockError} addTypename={true}>
          <ForcesIndicatorsView {...mockProps} />
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
          <ForcesIndicatorsView {...mockProps} />
        </MockedProvider>
      </Provider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });
});
