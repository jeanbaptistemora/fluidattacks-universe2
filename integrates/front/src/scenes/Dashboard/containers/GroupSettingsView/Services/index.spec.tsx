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
import { MemoryRouter } from "react-router-dom";
import wait from "waait";
import waitForExpect from "wait-for-expect";

import { GET_GROUP_DATA as GET_GROUP_SERVICES } from "scenes/Dashboard/containers/GroupRoute/queries";
import {
  GET_GROUP_DATA,
  UPDATE_GROUP_DATA,
} from "scenes/Dashboard/containers/GroupSettingsView/queries";
import { Services } from "scenes/Dashboard/containers/GroupSettingsView/Services";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

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
            hasMachine: true,
            hasSquad: true,
            language: "EN",
            name: "unittesting",
            service: "WHITE",
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
            hasMachine: true,
            hasSquad: true,
            language: "EN",
            name: "unittesting",
            service: "WHITE",
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
            hasMachine: true,
            hasSquad: true,
            language: "EN",
            name: "unittesting",
            service: "WHITE",
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
            hasMachine: false,
            hasSquad: false,
            language: "EN",
            name: "unittesting",
            service: "BLACK",
            subscription: "OnEsHoT",
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
            hasMachine: false,
            hasSquad: false,
            language: "EN",
            name: "unittesting",
            service: "WHITE",
            subscription: "CONTINUOUS",
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
            hasMachine: true,
            hasSquad: true,
            language: "EN",
            name: "unittesting",
            service: "WHITE",
            subscription: "CONTINUOUS",
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
            hasMachine: true,
            hasSquad: false,
            language: "EN",
            name: "unittesting",
            service: "WHITE",
            subscription: "CONTINUOUS",
          },
        },
      },
    },
  ];

  const mockedPermissions: PureAbility<string> = new PureAbility([
    { action: "api_mutations_update_group_mutate" },
  ]);

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Services).toStrictEqual("function");
  });

  [
    { group: "unittesting", rows: 4 },
    { group: "oneshottest", rows: 4 },
    { group: "not-exists", rows: 0 },
  ].forEach((test: { group: string; rows: number }): void => {
    it(`should render services for: ${test.group}`, async (): Promise<void> => {
      expect.hasAssertions();

      const wrapper: ReactWrapper = mount(
        <MockedProvider addTypename={false} mocks={mockResponses}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <MemoryRouter initialEntries={["/home"]}>
              <Services groupName={test.group} />
            </MemoryRouter>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      );
      await act(async (): Promise<void> => {
        const delay = 150;
        await wait(delay);
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

    const mockMutations: readonly MockedResponse[] = [
      {
        request: {
          query: UPDATE_GROUP_DATA,
          variables: {
            comments: "",
            description: "Integrates unit test project",
            groupName: "unittesting",
            hasASM: true,
            hasMachine: true,
            hasSquad: true,
            language: "EN",
            reason: "NONE",
            service: "WHITE",
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
          query: UPDATE_GROUP_DATA,
          variables: {
            comments: "",
            description: "Integrates unit test project",
            groupName: "unittesting",
            hasASM: true,
            hasMachine: false,
            hasSquad: false,
            language: "EN",
            reason: "NONE",
            service: "WHITE",
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
          query: UPDATE_GROUP_DATA,
          variables: {
            comments: "",
            description: "Integrates unit test project",
            groupName: "unittesting",
            hasASM: true,
            hasMachine: true,
            hasSquad: false,
            language: "EN",
            reason: "NONE",
            service: "WHITE",
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

    const wrapper: ReactWrapper = mount(
      <MockedProvider
        addTypename={false}
        mocks={[...mockResponses, ...mockMutations]}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MemoryRouter initialEntries={["/home"]}>
            <Services groupName={"unittesting"} />
          </MemoryRouter>
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await act(async (): Promise<void> => {
      const delay = 150;
      await wait(delay);
      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
      });
    });

    // Wrappers are functions because references get rapidly changed
    const table: () => ReactWrapper = (): ReactWrapper => wrapper.find("table");
    const tableBody: () => ReactWrapper = (): ReactWrapper =>
      table().find("tbody");
    const rows: () => ReactWrapper = (): ReactWrapper => tableBody().find("tr");

    const typeRow: () => ReactWrapper = (): ReactWrapper => rows().at(0);
    const serviceRow = rows().at(1);
    const machineRow = (): ReactWrapper => rows().at(2);
    const squadRowIndex = 3;
    const squadRow = (): ReactWrapper => rows().at(squadRowIndex);

    const serviceRowLeft = serviceRow.find("td").first();
    const typeRowLeft: () => ReactWrapper = (): ReactWrapper =>
      typeRow().find("td").first();
    const machineRowLeft = (): ReactWrapper => machineRow().find("td").first();
    const squadRowLeft: () => ReactWrapper = (): ReactWrapper =>
      squadRow().find("td").first();

    const totalRows = 4;

    expect(rows()).toHaveLength(totalRows);
    expect(typeRowLeft().text()).toStrictEqual("Subscription type");
    expect(serviceRowLeft.text()).toStrictEqual("Service");
    expect(machineRowLeft().text()).toStrictEqual("Machine");
    expect(squadRowLeft().text()).toStrictEqual("Squad");

    const machineSwitch = (): ReactWrapper =>
      machineRow().find("#machineSwitch").at(0);
    const squadSwitch: () => ReactWrapper = (): ReactWrapper =>
      squadRow().find("#squadSwitch").at(0);
    const formik: () => ReactWrapper = (): ReactWrapper =>
      wrapper.find("Formik").first();
    const proceedButton: () => ReactWrapper = (): ReactWrapper =>
      wrapper.find("Button").first();

    machineSwitch().simulate("click");

    expect(proceedButton().exists()).toStrictEqual(true);

    proceedButton().simulate("click");
    const confirmation: () => ReactWrapper = (): ReactWrapper =>
      wrapper.find({ name: "confirmation" }).find("input");
    confirmation().simulate("change", {
      target: { name: "confirmation", value: "unittesting" },
    });
    formik().simulate("submit");

    await act(async (): Promise<void> => {
      const delay = 150;
      await wait(delay);
      wrapper.update();

      expect(wrapper).toHaveLength(1);
      expect(msgSuccess).toHaveBeenCalledTimes(0);
    });

    squadSwitch().simulate("click");

    expect(proceedButton().exists()).toStrictEqual(true);

    proceedButton().simulate("click");
    confirmation().simulate("change", {
      target: { name: "confirmation", value: "unittesting" },
    });
    formik().simulate("submit");
    await act(async (): Promise<void> => {
      const delay = 150;
      await wait(delay);
      wrapper.update();

      expect(wrapper).toHaveLength(1);
      expect(msgSuccess).toHaveBeenCalledTimes(0);
    });

    squadSwitch().simulate("click");

    expect(proceedButton().exists()).toStrictEqual(true);

    proceedButton().simulate("click");
    confirmation().simulate("change", {
      target: { name: "confirmation", value: "unittesting" },
    });
    formik().simulate("submit");

    await act(async (): Promise<void> => {
      const delay = 150;
      await wait(delay);
      wrapper.update();
      const calls = 0;

      expect(wrapper).toHaveLength(1);
      expect(msgSuccess).toHaveBeenCalledTimes(calls);
    });

    jest.clearAllMocks();
  });
});
