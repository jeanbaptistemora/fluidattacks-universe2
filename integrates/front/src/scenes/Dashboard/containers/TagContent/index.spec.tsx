import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { Route } from "react-router";
import { MemoryRouter } from "react-router-dom";
import { TagContent } from "scenes/Dashboard/containers/TagContent";
import { TAG_QUERY } from "scenes/Dashboard/containers/TagContent/TagInfo/queries";
import store from "store";

describe("TagContent", () => {

  const mocks: MockedResponse = {
    request: {
      query: TAG_QUERY,
      variables: {
        tagName: "TEST-PROJECTS",
      },
    },
    result: {
      data: {
        tag: {
          lastClosingVuln: 10,
          maxOpenSeverity: 5,
          maxSeverity: 6,
          meanRemediate: 20,
          meanRemediateCriticalSeverity: 10,
          meanRemediateHighSeverity: 15,
          meanRemediateLowSeverity: 25,
          meanRemediateMediumSeverity: 30,
          name: "TEST-PROJECTS",
          projects: [
            {
              closedVulnerabilities: 1,
              name: "test",
              openVulnerabilities: 3,
              totalFindings: 2,
              totalTreatment: JSON.stringify({ accepted: 1, inProgress: 0, acceptedUndefined: 1, undefined: 1 }),
            },
          ],
        },
      },
    },
  };

  it("should return a function", () => {
    expect(typeof (TagContent))
      .toEqual("function");
  });

  it("should render a component", () => {
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/testorg/portfolios/test-projects/indicators"]}>
        <Provider store={store}>
          <MockedProvider mocks={[mocks]} addTypename={false}>
            <Route path="/orgs/:organizationName/portfolios/:tagName/indicators" component={TagContent} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    expect(wrapper)
      .toHaveLength(1);
  });
});
