import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_TOE_INPUTS, UPDATE_TOE_INPUT } from "./queries";

import { GroupToeInputsView } from ".";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("groupToeInputsView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupToeInputsView).toBe("function");
  });

  it("should display group toe inputs", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedToeInputs: MockedResponse = {
      request: {
        query: GET_TOE_INPUTS,
        variables: {
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetBePresentUntil: true,
          canGetFirstAttackAt: true,
          canGetSeenFirstTimeBy: true,
          first: 150,
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            name: "unittesting",
            toeInputs: {
              __typename: "ToeInputsConnection",
              edges: [
                {
                  node: {
                    __typename: "ToeInput",
                    attackedAt: "2020-01-02T00:00:00-05:00",
                    bePresent: true,
                    component: "test.com/api/Test",
                    entryPoint: "idTest",
                    firstAttackAt: "2020-02-19T15:41:04+00:00",
                    hasVulnerabilities: false,
                    root: {
                      id: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                      nickname: "test_nickname",
                    },
                    rootId: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                    rootNickname: "test_nickname",
                    seenAt: "2000-01-01T05:00:00+00:00",
                    seenFirstTimeBy: "",
                  },
                },
                {
                  node: {
                    __typename: "ToeInput",
                    attackedAt: "2021-02-02T00:00:00-05:00",
                    bePresent: true,
                    component: "test.com/test/test.aspx",
                    entryPoint: "btnTest",
                    firstAttackAt: "",
                    hasVulnerabilities: true,
                    root: {
                      id: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                      nickname: "test_nickname",
                    },
                    rootId: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                    rootNickname: "test_nickname",
                    seenAt: "2020-03-14T00:00:00-05:00",
                    seenFirstTimeBy: "test@test.com",
                  },
                },
                {
                  node: {
                    __typename: "ToeInput",
                    attackedAt: "2021-02-11T00:00:00-05:00",
                    bePresent: false,
                    component: "test.com/test2/test.aspx",
                    entryPoint: "-",
                    hasVulnerabilities: true,
                    root: null,
                    rootId: "",
                    rootNickname: "",
                    seenAt: "2020-01-11T00:00:00-05:00",
                    seenFirstTimeBy: "test2@test.com",
                  },
                },
              ],
              pageInfo: {
                endCursor: "bnVsbA==",
                hasNextPage: false,
              },
            },
          },
        },
      },
    };
    const mockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_toe_input_attacked_at_resolve" },
      { action: "api_resolvers_toe_input_attacked_by_resolve" },
      { action: "api_resolvers_toe_input_be_present_until_resolve" },
      { action: "api_resolvers_toe_input_first_attack_at_resolve" },
      { action: "api_resolvers_toe_input_seen_first_time_by_resolve" },
    ]);
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/inputs"]}>
        <MockedProvider addTypename={true} mocks={[mockedToeInputs]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/inputs"}>
              <GroupToeInputsView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByText("test_nickname")[0]).toBeInTheDocument();
    });

    expect(
      screen.getAllByRole("row")[0].textContent?.replace(/[^a-zA-Z ]/gu, "")
    ).toStrictEqual(
      [
        "group.toe.inputs.root",
        "group.toe.inputs.entryPoint",
        "group.toe.inputs.status",
        "group.toe.inputs.seenAt",
        "group.toe.inputs.attackedAt",
        "group.toe.inputs.seenFirstTimeBy",
      ]
        .join("")
        .replace(/[^a-zA-Z ]/gu, "")
    );

    expect(
      screen.getAllByRole("row")[1].textContent?.replace(/[^a-zA-Z ]/gu, "")
    ).toStrictEqual(
      [
        "test_nickname",
        "idTest",
        "Group.toe.inputs.safe",
        "2000-01-01",
        "2020-01-02",
        "",
      ]
        .join("")
        .replace(/[^a-zA-Z ]/gu, "")
    );
    expect(
      screen.getAllByRole("row")[2].textContent?.replace(/[^a-zA-Z ]/gu, "")
    ).toStrictEqual(
      [
        "test_nickname",
        "btnTest",
        "Group.toe.inputs.vulnerable",
        "2020-03-14",
        "2021-02-02",
        "test@test.com",
      ]
        .join("")
        .replace(/[^a-zA-Z ]/gu, "")
    );
    expect(
      screen.getAllByRole("row")[3].textContent?.replace(/[^a-zA-Z ]/gu, "")
    ).toStrictEqual(
      [
        "",
        "-",
        "Group.toe.inputs.vulnerable",
        "2020-01-11",
        "2021-02-11",
        "test2@test.com",
      ]
        .join("")
        .replace(/[^a-zA-Z ]/gu, "")
    );
  });

  it("should edit be present on cell", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UPDATE_TOE_INPUT,
          variables: {
            bePresent: false,
            canGetAttackedAt: true,
            canGetAttackedBy: true,
            canGetBePresentUntil: true,
            canGetFirstAttackAt: true,
            canGetSeenFirstTimeBy: true,
            component: "test.com/api/Test",
            entryPoint: "idTest",
            groupName: "unittesting",
            hasRecentAttack: undefined,
            rootId: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
            shouldGetNewToeInput: true,
          },
        },
        result: {
          data: {
            updateToeInput: {
              success: true,
              toeInput: {
                __typename: "ToeInput",
                attackedAt: "2020-01-02T00:00:00-05:00",
                bePresent: false,
                bePresentUntil: "2022-01-02T00:00:00-05:00",
                component: "test.com/api/Test",
                entryPoint: "idTest",
                firstAttackAt: "2020-02-19T15:41:04+00:00",
                hasVulnerabilities: false,
                root: {
                  id: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                  nickname: "test_nickname",
                },
                rootId: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                rootNickname: "test_nickname",
                seenAt: "2000-01-01T05:00:00+00:00",
                seenFirstTimeBy: "",
              },
            },
          },
        },
      },
    ];
    const mockedToeInputs: MockedResponse = {
      request: {
        query: GET_TOE_INPUTS,
        variables: {
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetBePresentUntil: true,
          canGetFirstAttackAt: true,
          canGetSeenFirstTimeBy: true,
          first: 150,
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            name: "unittesting",
            toeInputs: {
              __typename: "ToeInputsConnection",
              edges: [
                {
                  node: {
                    __typename: "ToeInput",
                    attackedAt: "2020-01-02T00:00:00-05:00",
                    bePresent: true,
                    bePresentUntil: null,
                    component: "test.com/api/Test",
                    entryPoint: "idTest",
                    firstAttackAt: "2020-02-19T15:41:04+00:00",
                    hasVulnerabilities: false,
                    root: {
                      id: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                      nickname: "test_nickname",
                    },
                    rootId: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                    rootNickname: "test_nickname",
                    seenAt: "2000-01-01T05:00:00+00:00",
                    seenFirstTimeBy: "",
                  },
                },
                {
                  node: {
                    __typename: "ToeInput",
                    attackedAt: "2021-02-02T00:00:00-05:00",
                    bePresent: true,
                    bePresentUntil: null,
                    component: "test.com/test/test.aspx",
                    entryPoint: "btnTest",
                    firstAttackAt: "",
                    hasVulnerabilities: true,
                    root: {
                      id: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                      nickname: "test_nickname",
                    },
                    rootId: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                    rootNickname: "test_nickname",
                    seenAt: "2020-03-14T00:00:00-05:00",
                    seenFirstTimeBy: "test@test.com",
                  },
                },
                {
                  node: {
                    __typename: "ToeInput",
                    attackedAt: "2021-02-11T00:00:00-05:00",
                    bePresent: false,
                    bePresentUntil: "2021-02-12T00:00:00-05:00",
                    component: "test.com/test2/test.aspx",
                    entryPoint: "-",
                    hasVulnerabilities: true,
                    root: null,
                    rootId: "",
                    rootNickname: "",
                    seenAt: "2020-01-11T00:00:00-05:00",
                    seenFirstTimeBy: "test2@test.com",
                  },
                },
              ],
              pageInfo: {
                endCursor: "bnVsbA==",
                hasNextPage: false,
              },
            },
          },
        },
      },
    };
    const mockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_toe_input_attacked_at_resolve" },
      { action: "api_resolvers_toe_input_attacked_by_resolve" },
      { action: "api_resolvers_toe_input_be_present_until_resolve" },
      { action: "api_resolvers_toe_input_first_attack_at_resolve" },
      { action: "api_resolvers_toe_input_seen_first_time_by_resolve" },
      { action: "api_mutations_update_toe_input_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/inputs"]}>
        <MockedProvider
          addTypename={true}
          mocks={[mockedToeInputs].concat(mocksMutation)}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/inputs"}>
              <GroupToeInputsView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByText("test_nickname")[0]).toBeInTheDocument();
    });

    await userEvent.click(
      screen.getByRole("button", { name: "group.findings.tableSet.btn.text" })
    );

    await userEvent.click(
      screen.getByRole("checkbox", {
        checked: false,
        name: "bePresent",
      })
    );
    await userEvent.click(
      screen.getByRole("checkbox", {
        checked: false,
        name: "bePresentUntil",
      })
    );

    expect(
      screen.getAllByRole("row")[0].textContent?.replace(/[^a-zA-Z ]/gu, "")
    ).toStrictEqual(
      [
        "group.toe.inputs.root",
        "group.toe.inputs.entryPoint",
        "group.toe.inputs.status",
        "group.toe.inputs.seenAt",
        "group.toe.inputs.bePresent",
        "group.toe.inputs.attackedAt",
        "group.toe.inputs.seenFirstTimeBy",
        "group.toe.inputs.bePresentUntil",
      ]
        .join("")
        .replace(/[^a-zA-Z ]/gu, "")
    );

    const row = screen.getByRole("row", {
      name: "test_nickname idTest Group.toe.inputs.safe 2000-01-01 bePresentSwitch Yes 2020-01-02",
    });

    await userEvent.click(
      within(row).getByRole("checkbox", { name: "bePresentSwitch" })
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.toe.inputs.alerts.updateInput",
        "groupAlerts.updatedTitle"
      );
    });
  });

  it("should mark input as attacked", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UPDATE_TOE_INPUT,
          variables: {
            bePresent: true,
            canGetAttackedAt: true,
            canGetAttackedBy: true,
            canGetBePresentUntil: true,
            canGetFirstAttackAt: true,
            canGetSeenFirstTimeBy: true,
            component: "test.com/api/Test",
            entryPoint: "idTest",
            groupName: "unittesting",
            hasRecentAttack: true,
            rootId: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
            shouldGetNewToeInput: false,
          },
        },
        result: {
          data: {
            updateToeInput: {
              success: true,
            },
          },
        },
      },
    ];
    const mockedToeInputs: MockedResponse = {
      request: {
        query: GET_TOE_INPUTS,
        variables: {
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetBePresentUntil: true,
          canGetFirstAttackAt: true,
          canGetSeenFirstTimeBy: true,
          first: 150,
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            name: "unittesting",
            toeInputs: {
              __typename: "ToeInputsConnection",
              edges: [
                {
                  node: {
                    __typename: "ToeInput",
                    attackedAt: "2020-01-02T00:00:00-05:00",
                    bePresent: true,
                    bePresentUntil: null,
                    component: "test.com/api/Test",
                    entryPoint: "idTest",
                    firstAttackAt: "2020-02-19T15:41:04+00:00",
                    hasVulnerabilities: false,
                    root: {
                      id: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                      nickname: "test_nickname",
                    },
                    rootId: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                    rootNickname: "test_nickname",
                    seenAt: "2000-01-01T05:00:00+00:00",
                    seenFirstTimeBy: "",
                  },
                },
              ],
              pageInfo: {
                endCursor: "bnVsbA==",
                hasNextPage: false,
              },
            },
          },
        },
      },
    };
    const mockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_toe_input_attacked_at_resolve" },
      { action: "api_resolvers_toe_input_attacked_by_resolve" },
      { action: "api_resolvers_toe_input_be_present_until_resolve" },
      { action: "api_resolvers_toe_input_first_attack_at_resolve" },
      { action: "api_resolvers_toe_input_seen_first_time_by_resolve" },
      { action: "api_mutations_update_toe_input_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/inputs"]}>
        <MockedProvider
          addTypename={true}
          mocks={[mockedToeInputs].concat(mocksMutation)}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/inputs"}>
              <GroupToeInputsView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    await userEvent.click(screen.getAllByRole("checkbox", { name: "" })[0]);
    await userEvent.click(
      screen.getByRole("button", {
        name: "group.toe.inputs.actionButtons.attackedButton.text",
      })
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.toe.inputs.alerts.markAsAttacked.success",
        "groupAlerts.updatedTitle"
      );
    });
  });
});
