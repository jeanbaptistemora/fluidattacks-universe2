import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import wait from "waait";
import store from "../../../../../store/index";
import { authzContext } from "../../../../../utils/authz/config";
import { GET_GROUP_DATA } from "../queries";
import { Services } from "./index";

describe("Services", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  const mockResponses: ReadonlyArray<MockedResponse> = [
    {
      request: {
        query: GET_GROUP_DATA,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          project: {
            hasDrills: true,
            hasForces: true,
            subscription: "CoNtInUoUs",
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_DATA,
        variables: {
          groupName : "oneshottest",
        },
      },
      result: {
        data: {
          project: {
            hasDrills: false,
            hasForces: false,
            subscription: "OnEsHoT",
          },
        },
      },
    },
  ];

  const mockedPermissions: PureAbility<string> = new PureAbility([
    { action: "backend_api_resolvers_project__do_edit_group" },
  ]);

  it("should return a function", () => {
    expect(typeof Services)
      .toEqual("function");
  });

  [
    { group: "unittesting", rows: 4 },
    { group: "oneshottest", rows: 2 },
    { group: "not-exists", rows: 0},
  ].forEach((test: { group: string; rows: number}) => {
    it(`should render services for: ${test.group}`, async () => {
      const wrapper: ReactWrapper = mount(
        <Provider store={store}>
          <MockedProvider mocks={mockResponses} addTypename={false}>
            <authzContext.Provider value={mockedPermissions}>
              <Services groupName={test.group} />
            </authzContext.Provider>
          </MockedProvider>
        </Provider>,
      );
      await act(async () => { await wait(1); wrapper.update(); });

      const table: ReactWrapper = wrapper.find("table");
      const tableBody: ReactWrapper = table.find("tbody");
      const rows: ReactWrapper = tableBody.find("tr");

      expect(rows)
        .toHaveLength(test.rows);
    });
  });
});
