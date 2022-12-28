import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_TOE_PORTS, UPDATE_TOE_PORT } from "./queries";
import type { IToePortsConnection } from "./types";

import { GroupToePortsView } from ".";
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

describe("groupToePortsView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupToePortsView).toBe("function");
  });

  it("should display group toe ports", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedToePorts: MockedResponse<{
      group: { name: string; toePorts: IToePortsConnection };
    }> = {
      request: {
        query: GET_TOE_PORTS,
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
            toePorts: {
              __typename: "ToePortsConnection",
              edges: [
                {
                  node: {
                    __typename: "ToePort",
                    address: "127.0.0.1",
                    attackedAt: "2020-01-02T00:00:00-05:00",
                    attackedBy: "hacker@test.com",
                    bePresent: true,
                    bePresentUntil: null,
                    firstAttackAt: "2020-02-19T15:41:04+00:00",
                    hasVulnerabilities: false,
                    port: 8080,
                    root: {
                      __typename: "IPRoot",
                      id: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                      nickname: "test_nickname",
                    },
                    seenAt: "2000-01-01T05:00:00+00:00",
                    seenFirstTimeBy: "",
                  },
                },
                {
                  node: {
                    __typename: "ToePort",
                    address: "172.16.0.0",
                    attackedAt: "2021-02-02T00:00:00-05:00",
                    attackedBy: "hacker@test.com",
                    bePresent: true,
                    bePresentUntil: null,
                    firstAttackAt: "2021-02-02T00:00:00-05:00",
                    hasVulnerabilities: true,
                    port: 8081,
                    root: {
                      __typename: "IPRoot",
                      id: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                      nickname: "test_nickname",
                    },
                    seenAt: "2020-03-14T00:00:00-05:00",
                    seenFirstTimeBy: "test@test.com",
                  },
                },
                {
                  node: {
                    __typename: "ToePort",
                    address: "172.31.255.255",
                    attackedAt: "2021-02-11T00:00:00-05:00",
                    attackedBy: "hacker@test.com",
                    bePresent: false,
                    bePresentUntil: "2021-03-11T00:00:00-05:00",
                    firstAttackAt: "2021-02-11T00:00:00-05:00",
                    hasVulnerabilities: true,
                    port: 80,
                    root: null,
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
      { action: "api_resolvers_toe_port_attacked_at_resolve" },
      { action: "api_resolvers_toe_port_attacked_by_resolve" },
      { action: "api_resolvers_toe_port_be_present_until_resolve" },
      { action: "api_resolvers_toe_port_first_attack_at_resolve" },
      { action: "api_resolvers_toe_port_seen_first_time_by_resolve" },
    ]);
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/ports"]}>
        <MockedProvider addTypename={true} mocks={[mockedToePorts]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/ports"}>
              <GroupToePortsView isInternal={true} />
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
        "group.toe.ports.root",
        "group.toe.ports.port",
        "group.toe.ports.status",
        "group.toe.ports.seenAt",
        "group.toe.ports.attackedAt",
        "group.toe.ports.seenFirstTimeBy",
      ]
        .join("")
        .replace(/[^a-zA-Z ]/gu, "")
    );
    expect(
      screen.getAllByRole("row")[1].textContent?.replace(/[^a-zA-Z ]/gu, "")
    ).toStrictEqual(
      [
        "test_nickname",
        "8080",
        "Group.toe.ports.safe",
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
        "8081",
        "Group.toe.ports.vulnerable",
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
        "80",
        "Group.toe.ports.vulnerable",
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
          query: UPDATE_TOE_PORT,
          variables: {
            address: "127.0.0.1",
            bePresent: false,
            canGetAttackedAt: true,
            canGetAttackedBy: true,
            canGetBePresentUntil: true,
            canGetFirstAttackAt: true,
            canGetSeenFirstTimeBy: true,
            groupName: "unittesting",
            hasRecentAttack: undefined,
            port: 8080,
            rootId: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
            shouldGetNewToePort: true,
          },
        },
        result: {
          data: {
            updateToePort: {
              success: true,
              toePort: {
                __typename: "ToePort",
                address: "127.0.0.1",
                attackedAt: "2020-01-02T00:00:00-05:00",
                attackedBy: "hacker@test.com",
                bePresent: false,
                bePresentUntil: "2022-01-02T00:00:00-05:00",
                firstAttackAt: "2020-02-19T15:41:04+00:00",
                hasVulnerabilities: false,
                port: 8080,
                root: {
                  __typename: "IPRoot",
                  id: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                  nickname: "test_nickname",
                },
                seenAt: "2000-01-01T05:00:00+00:00",
                seenFirstTimeBy: "",
              },
            },
          },
        },
      },
    ];
    const mockedToePorts: MockedResponse<{
      group: { name: string; toePorts: IToePortsConnection };
    }> = {
      request: {
        query: GET_TOE_PORTS,
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
            toePorts: {
              __typename: "ToePortsConnection",
              edges: [
                {
                  node: {
                    __typename: "ToePort",
                    address: "127.0.0.1",
                    attackedAt: "2020-01-02T00:00:00-05:00",
                    attackedBy: "hacker@test.com",
                    bePresent: true,
                    bePresentUntil: null,
                    firstAttackAt: "2020-02-19T15:41:04+00:00",
                    hasVulnerabilities: false,
                    port: 8080,
                    root: {
                      __typename: "IPRoot",
                      id: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                      nickname: "test_nickname",
                    },
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
      { action: "api_resolvers_toe_port_attacked_at_resolve" },
      { action: "api_resolvers_toe_port_attacked_by_resolve" },
      { action: "api_resolvers_toe_port_be_present_until_resolve" },
      { action: "api_resolvers_toe_port_first_attack_at_resolve" },
      { action: "api_resolvers_toe_port_seen_first_time_by_resolve" },
      { action: "api_mutations_update_toe_port_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/ports"]}>
        <MockedProvider
          addTypename={true}
          mocks={[mockedToePorts, ...mocksMutation]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/ports"}>
              <GroupToePortsView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
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
        "group.toe.ports.root",
        "group.toe.ports.port",
        "group.toe.ports.status",
        "group.toe.ports.seenAt",
        "group.toe.ports.bePresent",
        "group.toe.ports.attackedAt",
        "group.toe.ports.seenFirstTimeBy",
        "group.toe.ports.bePresentUntil",
      ]
        .join("")
        .replace(/[^a-zA-Z ]/gu, "")
    );

    const row = screen.getByRole("row", {
      name: "test_nickname 8080 Group.toe.ports.safe 2000-01-01 bePresentSwitch Yes 2020-01-02",
    });

    await userEvent.click(
      within(row).getByRole("checkbox", { name: "bePresentSwitch" })
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.toe.ports.alerts.updatePort",
        "groupAlerts.updatedTitle"
      );
    });
  });

  it("should mark port as attacked", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UPDATE_TOE_PORT,
          variables: {
            address: "127.0.0.1",
            bePresent: true,
            canGetAttackedAt: true,
            canGetAttackedBy: true,
            canGetBePresentUntil: true,
            canGetFirstAttackAt: true,
            canGetSeenFirstTimeBy: true,
            groupName: "unittesting",
            hasRecentAttack: true,
            port: 8080,
            rootId: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
            shouldGetNewToePort: false,
          },
        },
        result: {
          data: {
            updateToePort: {
              success: true,
            },
          },
        },
      },
    ];
    const mockedToePorts: MockedResponse<{
      group: { name: string; toePorts: IToePortsConnection };
    }> = {
      request: {
        query: GET_TOE_PORTS,
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
            toePorts: {
              __typename: "ToePortsConnection",
              edges: [
                {
                  node: {
                    __typename: "ToePort",
                    address: "127.0.0.1",
                    attackedAt: "2020-01-02T00:00:00-05:00",
                    attackedBy: "hacker@test.com",
                    bePresent: true,
                    bePresentUntil: null,
                    firstAttackAt: "2020-02-19T15:41:04+00:00",
                    hasVulnerabilities: false,
                    port: 8080,
                    root: {
                      __typename: "IPRoot",
                      id: "1a32cab8-7b4c-4761-a0a5-85cb8b64ce68",
                      nickname: "test_nickname",
                    },
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
      { action: "api_resolvers_toe_port_attacked_at_resolve" },
      { action: "api_resolvers_toe_port_attacked_by_resolve" },
      { action: "api_resolvers_toe_port_be_present_until_resolve" },
      { action: "api_resolvers_toe_port_first_attack_at_resolve" },
      { action: "api_resolvers_toe_port_seen_first_time_by_resolve" },
      { action: "api_mutations_update_toe_port_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/ports"]}>
        <MockedProvider
          addTypename={true}
          mocks={[mockedToePorts, ...mocksMutation]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/ports"}>
              <GroupToePortsView isInternal={true} />
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
        name: "group.toe.ports.actionButtons.attackedButton.text",
      })
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.toe.ports.alerts.markAsAttacked.success",
        "groupAlerts.updatedTitle"
      );
    });
  });
});
