import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { configure, mount, ReactWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import store from "../../../../../store";
import { TagsInfo, TagsProps } from "./index";
import { TAG_QUERY } from "./queries";

configure({ adapter: new ReactSixteenAdapter() });

describe("Tag Info", () => {

  const baseMockProps: TagsProps = {
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
      params: { tagName: "test-projects" },
      path: "/",
      url: "",
    },
  };

  const tagQuery: Readonly<MockedResponse> = {
    request: {
      query: TAG_QUERY,
      variables: {
        tag: "test-projects",
      },
    },
    result: {
      data: {
        tag: {
          name: "TEST-PROJECTS",
          projects: [
            {
              closedVulnerabilities: 1,
              lastClosingVuln: 10,
              maxOpenSeverity: 5,
              maxSeverity: 6,
              meanRemediate: 20,
              meanRemediateCriticalSeverity: 10,
              meanRemediateHighSeverity: 15,
              meanRemediateLowSeverity: 25,
              meanRemediateMediumSeverity: 30,
              name: "test1",
              openVulnerabilities: 3,
              totalFindings: 2,
              totalTreatment: JSON.stringify({ accepted: 1, inProgress: 0, acceptedUndefined: 1, undefined: 1 }),
            },
            {
              closedVulnerabilities: 3,
              lastClosingVuln: 3,
              maxOpenSeverity: 8,
              maxSeverity: 9,
              meanRemediate: 10,
              meanRemediateCriticalSeverity: 5,
              meanRemediateHighSeverity: 10,
              meanRemediateLowSeverity: 15,
              meanRemediateMediumSeverity: 20,
              name: "test2",
              openVulnerabilities: 5,
              totalFindings: 3,
              totalTreatment: JSON.stringify({ accepted: 1, inProgress: 3, acceptedUndefined: 0, undefined: 1 }),
            },
          ],
        },
      },
    },
  };

  it("should return a function", () => {
    expect(typeof (TagsInfo))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[tagQuery]} addTypename={false}>
          <TagsInfo {...baseMockProps} />
        </MockedProvider>
      </Provider>,
    );

    await act(async () => { await wait(10); wrapper.update(); });

    expect(wrapper)
      .toHaveLength(1);
  });
});
