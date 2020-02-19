import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { GraphQLError } from "graphql";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import * as React from "react";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import wait from "waait";
import store from "../../../../store/index";
import { GET_VULNERABILITIES } from "../../components/Vulnerabilities/queries";
import FindingContent from "./index";
import { IFindingContentProps } from "./types";

configure({ adapter: new ReactSixteenAdapter() });

const functionMock: (() => void) = (): void => undefined;

describe("FindingContent", () => {

  const mockProps: IFindingContentProps = {
    match: {
      isExact: true,
      params: { findingId: "438679960", projectName: "TEST" },
      path: "/",
      url: "",
    },
    onConfirmDelete: functionMock,
    onDelete: functionMock,
    onLoad: functionMock,
    onReject: functionMock,
    onUnmount: functionMock,
    userRole: "customer",
  };

  const mocks: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_VULNERABILITIES,
        variables: {
          identifier: "438679960",
        },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            id: "438679960",
            inputsVulns: [{
              __typename: "Vulnerability",
              currentState: "open",
              findingId: "438679960",
              id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
              specific: "email",
              treatment: "New",
              vulnType: "inputs",
              where: "https://example.com/contact",
            }],
            linesVulns: [],
            portsVulns: [],
            releaseDate: "2019-03-12 00:00:00",
            success: true,
          },
        },
      },
    },
  ];

  const mockError: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_VULNERABILITIES,
        variables: {
          identifier: "438679960",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a object", () => {
    expect(typeof (FindingContent))
      .toEqual("object");
  });

  it("should render an error in component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={mockError} addTypename={true}>
            <FindingContent {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <MemoryRouter initialEntries={["/project/TEST/findings/438679960/description"]}>
        <Provider store={store}>
          <MockedProvider mocks={mocks} addTypename={true}>
            <FindingContent {...mockProps} />
          </MockedProvider>
        </Provider>
      </MemoryRouter>,
    );
    await wait(0);
    expect(wrapper)
      .toHaveLength(1);
  });
});
