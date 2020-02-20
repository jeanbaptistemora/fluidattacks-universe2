import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { configure, mount, ReactWrapper, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import wait from "waait";
import store from "../../../../store";
import { FindingContent } from "./index";
import { GET_FINDING_HEADER } from "./queries";
import { IFindingContentProps } from "./types";

configure({ adapter: new ReactSixteenAdapter() });

describe("FindingContent", () => {

  const mockProps: IFindingContentProps = {
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
      params: { findingId: "438679960", projectName: "TEST" },
      path: "/",
      url: "",
    },
  };

  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_FINDING_HEADER,
        variables: {
          findingId: "438679960",
          submissionField: true,
        },
      },
      result: {
        data: {
          finding: {
            closedVulns: 0,
            historicState: [
              {
                analyst: "someone@fluidattacks.com",
                date: "2019-10-31 10:00:53",
                state: "CREATED",
              },
            ],
            id: "438679960",
            openVulns: 3,
            releaseDate: "2018-12-04 09:04:13",
            reportDate: "2017-12-04 09:04:13",
            severityScore: 2.6,
            state: "open",
            title: "FIN.S.0050. Weak passwords discovered",
          },
        },
      },
    },
  ];

  it("should return a object", () => {
    expect(typeof (FindingContent))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <MockedProvider mocks={mocks} addTypename={false}>
        <FindingContent {...mockProps} />
      </MockedProvider>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render header", async () => {
    (window as typeof window & { userRole: string }).userRole = "analyst";
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <FindingContent {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await act(async () => { await wait(0); wrapper.update(); });
    expect(wrapper.text())
      .toContain("FIN.S.0050. Weak passwords discovered");
  });
});
