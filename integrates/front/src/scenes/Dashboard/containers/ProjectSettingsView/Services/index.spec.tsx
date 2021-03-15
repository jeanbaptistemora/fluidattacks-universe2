/* eslint-disable @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
 -- Annotations added due to extended usage of "any" type in enzyme lib
 */
import { MemoryRouter } from "react-router-dom";
import { MockedProvider } from "@apollo/react-testing";
import type { MockedResponse } from "@apollo/react-testing";
import { Provider } from "react-redux";
import { PureAbility } from "@casl/ability";
import React from "react";
import type { ReactWrapper } from "enzyme";
import { Services } from "scenes/Dashboard/containers/ProjectSettingsView/Services";
import { act } from "react-dom/test-utils";
import { authzPermissionsContext } from "utils/authz/config";
import { mount } from "enzyme";
import store from "store";
import wait from "waait";
import {
  EDIT_GROUP_DATA,
  GET_GROUP_DATA,
} from "scenes/Dashboard/containers/ProjectSettingsView/queries";

interface IFormValues {
  drills: boolean;
  forces: boolean;
  integrates: boolean;
  type: string;
}

describe("Services", (): void => {
  const mockResponses: readonly MockedResponse[] = [
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
          groupName: "oneshottest",
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

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Services).toStrictEqual("function");
  });

  [
    { group: "unittesting", rows: 4 },
    { group: "oneshottest", rows: 3 },
    { group: "not-exists", rows: 0 },
  ].forEach((test: { group: string; rows: number }): void => {
    it(`should render services for: ${test.group}`, async (): Promise<void> => {
      expect.hasAssertions();

      const wrapper: ReactWrapper = mount(
        <Provider store={store}>
          <MockedProvider addTypename={false} mocks={mockResponses}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <MemoryRouter initialEntries={["/home"]}>
                <Services groupName={test.group} />
              </MemoryRouter>
            </authzPermissionsContext.Provider>
          </MockedProvider>
        </Provider>
      );
      await act(
        async (): Promise<void> => {
          await wait(1);
          wrapper.update();
        }
      );

      const table: ReactWrapper = wrapper.find("table");
      const tableBody: ReactWrapper = table.find("tbody");
      const rows: ReactWrapper = tableBody.find("tr");

      expect(rows).toHaveLength(test.rows);

      jest.clearAllMocks();
    });
  });

  it("should toggle buttons properly", async (): Promise<void> => {
    expect.hasAssertions();

    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider addTypename={false} mocks={mockResponses}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <MemoryRouter initialEntries={["/home"]}>
              <Services groupName={"unittesting"} />
            </MemoryRouter>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>
    );
    await act(
      async (): Promise<void> => {
        await wait(0);
        wrapper.update();
      }
    );

    const formValues: () => IFormValues = (): IFormValues =>
      store.getState().form.editGroup.values;

    // Wrappers are functions because references get rapidly changed
    const table: () => ReactWrapper = (): ReactWrapper => wrapper.find("table");
    const tableBody: () => ReactWrapper = (): ReactWrapper =>
      table().find("tbody");
    const rows: () => ReactWrapper = (): ReactWrapper => tableBody().find("tr");

    const typeRow: () => ReactWrapper = (): ReactWrapper => rows().at(0);
    const integratesRow: () => ReactWrapper = (): ReactWrapper => rows().at(1);
    const drillsRow: () => ReactWrapper = (): ReactWrapper => rows().at(2);
    const TEST_FORCES_ROW_INDEX = 3;
    const forcesRow: () => ReactWrapper = (): ReactWrapper =>
      rows().at(TEST_FORCES_ROW_INDEX);

    const typeRowLeft: () => ReactWrapper = (): ReactWrapper =>
      typeRow().find("td").first();
    const integratesRowLeft: () => ReactWrapper = (): ReactWrapper =>
      integratesRow().find("td").first();
    const drillsRowLeft: () => ReactWrapper = (): ReactWrapper =>
      drillsRow().find("td").first();
    const forcesRowLeft: () => ReactWrapper = (): ReactWrapper =>
      forcesRow().find("td").first();

    expect(rows()).toHaveLength(4);
    expect(typeRowLeft().text()).toStrictEqual("Subscription type");
    expect(integratesRowLeft().text()).toStrictEqual("Integrates");
    expect(drillsRowLeft().text()).toStrictEqual("Drills");
    expect(forcesRowLeft().text()).toStrictEqual("Forces");

    const integratesSwitch: () => ReactWrapper = (): ReactWrapper =>
      integratesRow().find("#integratesSwitch").at(0);
    const drillsSwitch: () => ReactWrapper = (): ReactWrapper =>
      drillsRow().find("#drillsSwitch").at(0);
    const forcesSwitch: () => ReactWrapper = (): ReactWrapper =>
      forcesRow().find("#forcesSwitch").at(0);

    expect(formValues()).toStrictEqual({
      comments: "",
      confirmation: "",
      drills: true,
      forces: true,
      integrates: true,
      reason: "NONE",
      type: "CONTINUOUS",
    });

    integratesSwitch().simulate("click");

    expect(formValues()).toStrictEqual({
      comments: "",
      confirmation: "",
      drills: false,
      forces: false,
      integrates: false,
      reason: "NONE",
      type: "CONTINUOUS",
    });

    drillsSwitch().simulate("click");

    expect(formValues()).toStrictEqual({
      comments: "",
      confirmation: "",
      drills: true,
      forces: false,
      integrates: true,
      reason: "NONE",
      type: "CONTINUOUS",
    });

    drillsSwitch().simulate("click");

    expect(formValues()).toStrictEqual({
      comments: "",
      confirmation: "",
      drills: false,
      forces: false,
      integrates: true,
      reason: "NONE",
      type: "CONTINUOUS",
    });

    const proceedButton: () => ReactWrapper = (): ReactWrapper =>
      wrapper.find("Button").first();
    const genericForm: () => ReactWrapper = (): ReactWrapper =>
      wrapper.find("genericForm").first();

    expect(proceedButton().exists()).toStrictEqual(true);

    genericForm().simulate("submit");

    forcesSwitch().simulate("click");

    expect(formValues()).toStrictEqual({
      comments: "",
      confirmation: "",
      drills: true,
      forces: true,
      integrates: true,
      reason: "NONE",
      type: "CONTINUOUS",
    });

    drillsSwitch().simulate("click");

    expect(formValues()).toStrictEqual({
      comments: "",
      confirmation: "",
      drills: false,
      forces: false,
      integrates: true,
      reason: "NONE",
      type: "CONTINUOUS",
    });

    forcesSwitch().simulate("click");

    expect(formValues()).toStrictEqual({
      comments: "",
      confirmation: "",
      drills: true,
      forces: true,
      integrates: true,
      reason: "NONE",
      type: "CONTINUOUS",
    });

    jest.clearAllMocks();
  });
});
