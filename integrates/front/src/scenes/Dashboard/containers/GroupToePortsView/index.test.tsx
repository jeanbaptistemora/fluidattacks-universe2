import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_TOE_PORTS } from "./queries";
import type { IToePortsConnection } from "./types";

import { GroupToePortsView } from ".";
import { authzPermissionsContext } from "utils/authz/config";

jest.mock("../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

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
        "group.toe.ports.hasVulnerabilities",
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
        "group.toe.ports.no",
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
        "group.toe.ports.yes",
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
        "group.toe.ports.yes",
        "2020-01-11",
        "2021-02-11",
        "test2@test.com",
      ]
        .join("")
        .replace(/[^a-zA-Z ]/gu, "")
    );
  });
});
