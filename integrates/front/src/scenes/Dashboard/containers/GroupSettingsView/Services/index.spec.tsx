/* eslint-disable @typescript-eslint/no-unsafe-return, @typescript-eslint/no-unsafe-member-access
 -- Annotations added due to extended usage of "any" type in enzyme lib
 */
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import React from "react";
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { MemoryRouter } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { GET_GROUP_DATA as GET_GROUP_SERVICES } from "scenes/Dashboard/containers/GroupRoute/queries";
import {
  EDIT_GROUP_DATA,
  GET_GROUP_DATA,
} from "scenes/Dashboard/containers/GroupSettingsView/queries";
import { Services } from "scenes/Dashboard/containers/GroupSettingsView/Services";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";

interface IFormValues {
  squad: boolean;
  forces: boolean;
  asm: boolean;
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
          group: {
            hasForces: true,
            hasMachine: true,
            hasSquad: true,
            language: "EN",
            name: "unittesting",
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
          group: {
            hasForces: true,
            hasMachine: true,
            hasSquad: true,
            language: "EN",
            name: "unittesting",
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
          group: {
            hasForces: false,
            hasMachine: false,
            hasSquad: false,
            language: "EN",
            name: "unittesting",
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
          hasForces: false,
          hasMachine: false,
          hasSquad: false,
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
    {
      request: {
        query: GET_GROUP_SERVICES,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            hasForces: false,
            hasMachine: false,
            hasSquad: false,
            language: "EN",
            name: "unittesting",
            subscription: "CONTINUOUS",
          },
        },
      },
    },
  ];

  const mockedPermissions: PureAbility<string> = new PureAbility([
    { action: "api_mutations_edit_group_mutate" },
  ]);

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Services).toStrictEqual("function");
  });

  [
    { group: "unittesting", rows: 3 },
    { group: "oneshottest", rows: 2 },
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
      await act(async (): Promise<void> => {
        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper).toHaveLength(1);
        });
      });

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
    await act(async (): Promise<void> => {
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
      });
    });

    const formValues: () => IFormValues = (): IFormValues =>
      store.getState().form.editGroup.values;

    // Wrappers are functions because references get rapidly changed
    const table: () => ReactWrapper = (): ReactWrapper => wrapper.find("table");
    const tableBody: () => ReactWrapper = (): ReactWrapper =>
      table().find("tbody");
    const rows: () => ReactWrapper = (): ReactWrapper => tableBody().find("tr");

    const typeRow: () => ReactWrapper = (): ReactWrapper => rows().at(0);
    const machineRow = (): ReactWrapper => rows().at(1);
    const squadRowIndex = 2;
    const squadRow = (): ReactWrapper => rows().at(squadRowIndex);

    const typeRowLeft: () => ReactWrapper = (): ReactWrapper =>
      typeRow().find("td").first();
    const machineRowLeft = (): ReactWrapper => machineRow().find("td").first();
    const squadRowLeft: () => ReactWrapper = (): ReactWrapper =>
      squadRow().find("td").first();

    const totalRows = 3;

    expect(rows()).toHaveLength(totalRows);
    expect(typeRowLeft().text()).toStrictEqual("Subscription type");
    expect(machineRowLeft().text()).toStrictEqual("Machine");
    expect(squadRowLeft().text()).toStrictEqual("Squad");

    const machineSwitch = (): ReactWrapper =>
      machineRow().find("#machineSwitch").at(0);
    const squadSwitch: () => ReactWrapper = (): ReactWrapper =>
      squadRow().find("#squadSwitch").at(0);

    expect(formValues()).toStrictEqual({
      asm: true,
      comments: "",
      confirmation: "",
      machine: true,
      reason: "NONE",
      squad: true,
      type: "CONTINUOUS",
    });

    machineSwitch().simulate("click");

    expect(formValues()).toStrictEqual({
      asm: true,
      comments: "",
      confirmation: "",
      machine: false,
      reason: "NONE",
      squad: false,
      type: "CONTINUOUS",
    });

    const proceedButton: () => ReactWrapper = (): ReactWrapper =>
      wrapper.find("Button").first();

    expect(proceedButton().exists()).toStrictEqual(true);

    squadSwitch().simulate("click");

    expect(formValues()).toStrictEqual({
      asm: true,
      comments: "",
      confirmation: "",
      machine: true,
      reason: "NONE",
      squad: true,
      type: "CONTINUOUS",
    });

    const genericForm: () => ReactWrapper = (): ReactWrapper =>
      wrapper.find("genericForm").first();

    genericForm().simulate("submit");

    squadSwitch().simulate("click");

    expect(formValues()).toStrictEqual({
      asm: true,
      comments: "",
      confirmation: "",
      machine: true,
      reason: "NONE",
      squad: false,
      type: "CONTINUOUS",
    });

    jest.clearAllMocks();
  });
});
