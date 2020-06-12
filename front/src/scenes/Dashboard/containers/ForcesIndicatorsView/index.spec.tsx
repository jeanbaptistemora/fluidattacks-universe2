import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import { GraphQLError } from "graphql";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import store from "../../../../store/index";
import { ForcesIndicatorsView } from "./index";
import { GET_INDICATORS } from "./queries";
import {
  IForcesExecution, IForcesIndicatorsProps, IForcesIndicatorsViewBaseProps, IForcesVulnerabilities,
} from "./types";

describe("ForcesIndicatorsView", () => {

  it("should return an function", () => {
    expect(typeof (ForcesIndicatorsView))
      .toEqual("function");
  });

  it("should render an empty component", async () => {
    const mockProps: IForcesIndicatorsViewBaseProps = { projectName: "TEST" };

    const mockError: ReadonlyArray<MockedResponse> = [{
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

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/forces"]}>
        <Provider store={store}>
          <MockedProvider mocks={mockError} addTypename={false}>
            <ForcesIndicatorsView {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    await act(async () => { await wait(0); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render Forces Indicators", async () => {
    const mockProps: IForcesIndicatorsViewBaseProps = { projectName: "TEST" };

    const forcesVulnerabilities: IForcesVulnerabilities = {
      numOfVulnerabilitiesInAcceptedExploits: 1,
      numOfVulnerabilitiesInExploits: 2,
      numOfVulnerabilitiesInIntegratesExploits: 3,
    };

    const forcesExecution: IForcesExecution = {
      strictness: "strict",
      vulnerabilities: forcesVulnerabilities,
    };

    const forcesIndicators: IForcesIndicatorsProps = {
      forcesExecutions: {
        executions: [forcesExecution],
      },
      project: {
        hasForces: true,
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
          data: forcesIndicators,
        },
      }];

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/forces"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <ForcesIndicatorsView {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    expect(wrapper)
      .toHaveLength(1);

    await act(async () => { await wait(0); wrapper.update(); });

    const forcesIndicatorsTitle: ReactWrapper = wrapper.find("h1")
      .filterWhere((element: ReactWrapper) => element.contains("Forces Indicators"));
    const systemStatusWidget: ReactWrapper = wrapper
      .find("div")
      .filterWhere((element: ReactWrapper) => element.contains("System status"))
      .first();
    const ratioOfStrictBuildsWidget: ReactWrapper = wrapper
      .find("div")
      .filterWhere((element: ReactWrapper) => element.contains("Ratio of builds in Strict mode"))
      .first();
    const serviceUsageWidget: ReactWrapper = wrapper
      .find("div")
      .filterWhere((element: ReactWrapper) => element.contains("Service usage"))
      .first();
    const vulnerableBuildsWidget: ReactWrapper = wrapper
      .find("div")
      .filterWhere((element: ReactWrapper) => element.contains("Vulnerable builds"))
      .first();
    const protectedBuildsWidget: ReactWrapper = wrapper
      .find("div")
      .filterWhere((element: ReactWrapper) => element.contains("Protected builds"))
      .first();
    const buildsWithAcceptedRiskWidget: ReactWrapper = wrapper
      .find("div")
      .filterWhere((element: ReactWrapper) => element.contains("Builds with accepted risk"))
      .first();

    expect(wrapper)
      .toHaveLength(1);
    expect(forcesIndicatorsTitle)
      .toHaveLength(1);
    expect(systemStatusWidget)
      .toHaveLength(1);
    expect(ratioOfStrictBuildsWidget)
      .toHaveLength(1);
    expect(serviceUsageWidget)
      .toHaveLength(1);
    expect(protectedBuildsWidget)
      .toHaveLength(1);
    expect(vulnerableBuildsWidget)
      .toHaveLength(1);
    expect(buildsWithAcceptedRiskWidget)
      .toHaveLength(1);
  });
});
