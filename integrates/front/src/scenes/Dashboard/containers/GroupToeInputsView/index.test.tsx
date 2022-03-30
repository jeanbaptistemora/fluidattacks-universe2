import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_TOE_INPUTS } from "./queries";

import { GroupToeInputsView } from ".";
import { authzPermissionsContext } from "utils/authz/config";

describe("GroupToeInputsView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupToeInputsView).toStrictEqual("function");
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
    const mockedPermissions: PureAbility<string> = new PureAbility([
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
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(screen.getAllByRole("row")[0].textContent).toStrictEqual(
      [
        "group.toe.inputs.root",
        "group.toe.inputs.entryPoint",
        "group.toe.inputs.hasVulnerabilities",
        "group.toe.inputs.attackedAt",
        "group.toe.inputs.seenAt",
        "group.toe.inputs.seenFirstTimeBy",
      ].join("")
    );
    expect(screen.getAllByRole("row")[1].textContent).toStrictEqual(
      [
        "test_nickname",
        "idTest",
        "group.toe.inputs.no",
        "2020-01-02",
        "2000-01-01",
        "",
      ].join("")
    );
    expect(screen.getAllByRole("row")[2].textContent).toStrictEqual(
      [
        "test_nickname",
        "btnTest",
        "group.toe.inputs.yes",
        "2021-02-02",
        "2020-03-14",
        "test@test.com",
      ].join("")
    );

    const thirdRow: number = 3;

    expect(screen.getAllByRole("row")[thirdRow].textContent).toStrictEqual(
      [
        "",
        "-",
        "group.toe.inputs.yes",
        "2021-02-11",
        "2020-01-11",
        "test2@test.com",
      ].join("")
    );
  });
});
