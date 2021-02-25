import { MockedProvider, MockedResponse } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import * as React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import wait from "waait";

import { EDIT_GROUP_DATA, GET_GROUP_DATA } from "scenes/Dashboard/containers/ProjectSettingsView/queries";
import { Services } from "scenes/Dashboard/containers/ProjectSettingsView/Services";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";

interface IFormValues {
  drills: boolean;
  forces: boolean;
  integrates: boolean;
  type: string;
}

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
            language: "EN",
            subscription: "CoNtInUoUs",
          },
        },
      },
    },
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
            language: "EN",
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
            language: "EN",
            subscription: "OnEsHoT",
          },
        },
      },
    },
    {
      request: {
        query: EDIT_GROUP_DATA,
        variables: {
          groupName: "unittesting",
          hasDrills: false,
          hasForces: false,
          language: "EN",
          subscription: "CONTINUOUS",
        },
      },
      result: {
        data: {
          editGroup: {
            success: true,
          },
        },
      },
    },
  ];

  const mockedPermissions: PureAbility<string> = new PureAbility([
    { action: "backend_api_mutations_edit_group_mutate" },
  ]);

  it("should return a function", () => {
    expect(typeof Services)
      .toEqual("function");
  });

  [
    { group: "unittesting", rows: 4 },
    { group: "oneshottest", rows: 3 },
    { group: "not-exists", rows: 0},
  ].forEach((test: { group: string; rows: number}) => {
    it(`should render services for: ${test.group}`, async () => {
      const wrapper: ReactWrapper = mount(
        <Provider store={store}>
          <MockedProvider mocks={mockResponses} addTypename={false}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <MemoryRouter initialEntries={["/home"]}>
                <Services groupName={test.group} />
              </MemoryRouter>
            </authzPermissionsContext.Provider>
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

  it("should toggle buttons properly", async () => {
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={mockResponses} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <MemoryRouter initialEntries={["/home"]}>
              <Services groupName="unittesting" />
            </MemoryRouter>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(0); wrapper.update(); });

    const formValues: (() => IFormValues) = (): IFormValues => store.getState().form.editGroup.values;

    // Wrappers are functions because references get rapidly changed
    const table: (() => ReactWrapper) = (): ReactWrapper => wrapper.find("table");
    const tableBody: (() => ReactWrapper) = (): ReactWrapper =>
      table()
        .find("tbody");
    const rows: (() => ReactWrapper) = (): ReactWrapper =>
      tableBody()
        .find("tr");

    const typeRow: (() => ReactWrapper) = (): ReactWrapper =>
      rows()
        .at(0);
    const integratesRow: (() => ReactWrapper) = (): ReactWrapper =>
      rows()
        .at(1);
    const drillsRow: (() => ReactWrapper) = (): ReactWrapper =>
      rows()
        .at(2);
    const forcesRow: (() => ReactWrapper) = (): ReactWrapper =>
      rows()
        .at(3);

    const typeRowLeft: (() => ReactWrapper) = (): ReactWrapper =>
      typeRow()
        .find("td")
        .first();
    const integratesRowLeft: (() => ReactWrapper) = (): ReactWrapper =>
      integratesRow()
        .find("td")
        .first();
    const drillsRowLeft: (() => ReactWrapper) = (): ReactWrapper =>
      drillsRow()
        .find("td")
        .first();
    const forcesRowLeft: (() => ReactWrapper) = (): ReactWrapper =>
      forcesRow()
        .find("td")
        .first();

    expect(rows())
      .toHaveLength(4);
    expect(
      typeRowLeft()
        .text())
          .toEqual("Subscription type");
    expect(
      integratesRowLeft()
        .text())
          .toEqual("Integrates");
    expect(
      drillsRowLeft()
        .text())
          .toEqual("Drills");
    expect(
      forcesRowLeft()
        .text())
          .toEqual("Forces");

    const integratesSwitch: (() => ReactWrapper) = (): ReactWrapper =>
      integratesRow()
        .find("#integratesSwitch")
        .at(0);
    const drillsSwitch: (() => ReactWrapper) = (): ReactWrapper =>
      drillsRow()
        .find("#drillsSwitch")
        .at(0);
    const forcesSwitch: (() => ReactWrapper) = (): ReactWrapper =>
      forcesRow()
        .find("#forcesSwitch")
        .at(0);

    expect(formValues())
      .toEqual({
        comments: "",
        confirmation: "",
        drills: true,
        forces: true,
        integrates: true,
        reason: "NONE",
        type: "CONTINUOUS",
      });

    integratesSwitch()
      .simulate("click");

    expect(formValues())
      .toEqual({
        comments: "",
        confirmation: "",
        drills: false,
        forces: false,
        integrates: false,
        reason: "NONE",
        type: "CONTINUOUS",
      });

    drillsSwitch()
      .simulate("click");

    expect(formValues())
      .toEqual({
        comments: "",
        confirmation: "",
        drills: true,
        forces: false,
        integrates: true,
        reason: "NONE",
        type: "CONTINUOUS",
      });

    drillsSwitch()
      .simulate("click");

    expect(formValues())
      .toEqual({
        comments: "",
        confirmation: "",
        drills: false,
        forces: false,
        integrates: true,
        reason: "NONE",
        type: "CONTINUOUS",
      });

    const proceedButton: (() => ReactWrapper) = (): ReactWrapper =>
      wrapper
        .find("Button")
        .first();
    const genericForm: (() => ReactWrapper) = (): ReactWrapper =>
      wrapper
        .find("genericForm")
        .first();

    expect(
      proceedButton()
        .exists())
          .toEqual(true);

    genericForm()
      .simulate("submit");

    forcesSwitch()
      .simulate("click");

    expect(formValues())
      .toEqual({
        comments: "",
        confirmation: "",
        drills: true,
        forces: true,
        integrates: true,
        reason: "NONE",
        type: "CONTINUOUS",
      });

    drillsSwitch()
      .simulate("click");

    expect(formValues())
      .toEqual({
        comments: "",
        confirmation: "",
        drills: false,
        forces: false,
        integrates: true,
        reason: "NONE",
        type: "CONTINUOUS",
      });

    forcesSwitch()
      .simulate("click");

    expect(formValues())
      .toEqual({
        comments: "",
        confirmation: "",
        drills: true,
        forces: true,
        integrates: true,
        reason: "NONE",
        type: "CONTINUOUS",
      });

  });
});
