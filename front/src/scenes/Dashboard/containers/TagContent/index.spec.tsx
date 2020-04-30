import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
import { Provider } from "react-redux";
import { MemoryRouter, RouteComponentProps } from "react-router-dom";
import store from "../../../../store/index";
import { TagContent } from "./index";
import { TAG_QUERY } from "./TagInfo/queries";

describe("TagContent", () => {

  const mockProps: RouteComponentProps<{ tagName: string }> = {
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
      params: { tagName: "TEST-PROJECTS" },
      path: "/",
      url: "",
    },
  };

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
      <MemoryRouter initialEntries={["/portfolio/TEST-PROJECTS/indicators"]}>
        <Provider store={store}>
          <MockedProvider mocks={[mocks]} addTypename={false}>
            <TagContent {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );

    expect(wrapper)
      .toHaveLength(1);
  });
});
