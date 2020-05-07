import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import wait from "waait";
import store from "../../../../store/index";
import { ForcesIndicatorsView } from "./index";
import { GET_INDICATORS } from "./queries";
import { IForcesIndicatorsViewBaseProps } from "./types";

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
                  numOfVulnerabilitiesInIntegratesExploits: 3,
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
      <MemoryRouter initialEntries={["/project/TEST/forces"]}>
        <Provider store={store}>
          <MockedProvider mocks={mockError} addTypename={true}>
            <ForcesIndicatorsView {...mockProps} />
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
      <MemoryRouter initialEntries={["/project/TEST/forces"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={true}>
            <ForcesIndicatorsView {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });
});
