import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_TOE_LINES, VERIFY_TOE_LINES } from "./queries";

import { GroupToeLinesView } from ".";
import { authzPermissionsContext } from "utils/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("groupToeLinesView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupToeLinesView).toBe("function");
  });

  it("should display group toe lines", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
          first: 150,
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            toeLines: {
              __typename: "ToeLinesConnection",
              edges: [
                {
                  __typename: "ToeLinesEdge",
                  node: {
                    __typename: "ToeLines",
                    attackedAt: "2021-02-20T05:00:00+00:00",
                    attackedBy: "test2@test.com",
                    attackedLines: 4,
                    bePresent: true,
                    bePresentUntil: "",
                    comments: "comment 1",
                    filename: "test/test#.config",
                    firstAttackAt: "2020-02-19T15:41:04+00:00",
                    hasVulnerabilities: false,
                    lastAuthor: "user@gmail.com",
                    lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                    loc: 8,
                    modifiedDate: "2020-11-15T15:41:04+00:00",
                    root: {
                      id: "63298a73-9dff-46cf-b42d-9b2f01a56690",
                      nickname: "product",
                    },
                    seenAt: "2020-02-01T15:41:04+00:00",
                    sortsRiskLevel: 80,
                  },
                },
                {
                  __typename: "ToeLinesEdge",
                  node: {
                    __typename: "ToeLines",
                    attackedAt: "",
                    attackedBy: "test@test.com",
                    attackedLines: 120,
                    bePresent: false,
                    bePresentUntil: "2021-01-01T15:41:04+00:00",
                    comments: "comment 2",
                    filename: "test2/test.sh",
                    firstAttackAt: "",
                    hasVulnerabilities: true,
                    lastAuthor: "user@gmail.com",
                    lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
                    loc: 172,
                    modifiedDate: "2020-11-16T15:41:04+00:00",
                    root: {
                      id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                      nickname: "integrates_1",
                    },
                    seenAt: "2020-01-01T15:41:04+00:00",
                    sortsRiskLevel: 0,
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
      { action: "api_resolvers_toe_lines_attacked_at_resolve" },
      { action: "api_resolvers_toe_lines_attacked_by_resolve" },
      { action: "api_resolvers_toe_lines_attacked_lines_resolve" },
      { action: "api_resolvers_toe_lines_be_present_until_resolve" },
      { action: "api_resolvers_toe_lines_comments_resolve" },
      { action: "api_resolvers_toe_lines_first_attack_at_resolve" },
      { action: "see_toe_lines_coverage" },
    ]);
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider addTypename={true} mocks={[mockedToeLines]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(screen.getAllByRole("row")[0].textContent).toStrictEqual(
      [
        "group.toe.lines.root",
        "group.toe.lines.coverage",
        "group.toe.lines.loc",
        "group.toe.lines.attackedLines",
        "group.toe.lines.hasVulnerabilities",
        "group.toe.lines.modifiedDate",
        "group.toe.lines.lastCommit",
        "group.toe.lines.attackedAt",
        "group.toe.lines.comments",
      ].join("")
    );
    expect(screen.getAllByRole("row")[1].textContent).toStrictEqual(
      [
        "integrates_1",
        "70%",
        "172",
        "120",
        "group.toe.lines.yes",
        "2020-11-16",
        "f9e4beb",
        "",
        "comment 2",
      ].join("")
    );
    expect(screen.getAllByRole("row")[2].textContent).toStrictEqual(
      [
        "product",
        "50%",
        "8",
        "4",
        "group.toe.lines.no",
        "2020-11-15",
        "f9e4beb",
        "2021-02-20",
        "comment 1",
      ].join("")
    );
  });

  it("should handle verify lines", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: VERIFY_TOE_LINES,
          variables: {
            canGetAttackedAt: true,
            canGetAttackedBy: true,
            canGetAttackedLines: true,
            canGetBePresentUntil: true,
            canGetComments: true,
            canGetFirstAttackAt: true,
            filename: "test/test#.config",
            groupName: "unittesting",
            rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
            shouldGetNewToeLines: false,
          },
        },
        result: { data: { updateToeLinesAttackedLines: { success: true } } },
      },
      {
        request: {
          query: VERIFY_TOE_LINES,
          variables: {
            canGetAttackedAt: true,
            canGetAttackedBy: true,
            canGetAttackedLines: true,
            canGetBePresentUntil: true,
            canGetComments: true,
            canGetFirstAttackAt: true,
            filename: "test2/test.sh",
            groupName: "unittesting",
            rootId: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            shouldGetNewToeLines: false,
          },
        },
        result: { data: { updateToeLinesAttackedLines: { success: true } } },
      },
    ];
    const mockedToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
          first: 150,
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            toeLines: {
              __typename: "ToeLinesConnection",
              edges: [
                {
                  __typename: "ToeLinesEdge",
                  node: {
                    __typename: "ToeLines",
                    attackedAt: "2021-02-20T05:00:00+00:00",
                    attackedBy: "test2@test.com",
                    attackedLines: 4,
                    bePresent: true,
                    bePresentUntil: "",
                    comments: "comment 1",
                    filename: "test/test#.config",
                    firstAttackAt: "2020-02-19T15:41:04+00:00",
                    hasVulnerabilities: false,
                    lastAuthor: "user@gmail.com",
                    lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                    loc: 8,
                    modifiedDate: "2020-11-15T15:41:04+00:00",
                    root: {
                      id: "63298a73-9dff-46cf-b42d-9b2f01a56690",
                      nickname: "product",
                    },
                    seenAt: "2020-02-01T15:41:04+00:00",
                    sortsRiskLevel: 80,
                    sortsSuggestions: null,
                  },
                },
                {
                  __typename: "ToeLinesEdge",
                  node: {
                    __typename: "ToeLines",
                    attackedAt: "",
                    attackedBy: "test@test.com",
                    attackedLines: 120,
                    bePresent: false,
                    bePresentUntil: "2021-01-01T15:41:04+00:00",
                    comments: "comment 2",
                    filename: "test2/test.sh",
                    firstAttackAt: "",
                    hasVulnerabilities: true,
                    lastAuthor: "user@gmail.com",
                    lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
                    loc: 172,
                    modifiedDate: "2020-11-16T15:41:04+00:00",
                    root: {
                      id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                      nickname: "integrates_1",
                    },
                    seenAt: "2020-01-01T15:41:04+00:00",
                    sortsRiskLevel: 0,
                    sortsSuggestions: null,
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
      { action: "api_resolvers_toe_lines_attacked_at_resolve" },
      { action: "api_resolvers_toe_lines_attacked_by_resolve" },
      { action: "api_resolvers_toe_lines_attacked_lines_resolve" },
      { action: "api_resolvers_toe_lines_be_present_until_resolve" },
      { action: "api_resolvers_toe_lines_comments_resolve" },
      { action: "api_resolvers_toe_lines_first_attack_at_resolve" },
      { action: "api_mutations_update_toe_lines_attacked_lines_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          mocks={[mockedToeLines, ...mocksMutation]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    userEvent.click(screen.getAllByRole("checkbox")[1]);
    userEvent.click(screen.getAllByRole("checkbox")[2]);

    userEvent.click(
      screen.getByText("group.toe.lines.actionButtons.verifyButton.text")
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.toe.lines.alerts.verifyToeLines.success",
        "groupAlerts.updatedTitle"
      );
    });
  });

  it("should handle edit attacked lines on cell", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: VERIFY_TOE_LINES,
          variables: {
            attackedLines: 6,
            canGetAttackedAt: true,
            canGetAttackedBy: true,
            canGetAttackedLines: true,
            canGetBePresentUntil: true,
            canGetComments: true,
            canGetFirstAttackAt: true,
            filename: "test/test#.config",
            groupName: "unittesting",
            rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
            shouldGetNewToeLines: true,
          },
        },
        result: {
          data: {
            updateToeLinesAttackedLines: {
              success: true,
              toeLines: {
                __typename: "ToeLines",
                attackedAt: "2021-02-20T05:00:00+00:00",
                attackedBy: "test2@test.com",
                attackedLines: 6,
                bePresent: true,
                bePresentUntil: "",
                comments: "comment 1",
                filename: "test/test#.config",
                firstAttackAt: "2020-02-19T15:41:04+00:00",
                hasVulnerabilities: false,
                lastAuthor: "user@gmail.com",
                lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                loc: 8,
                modifiedDate: "2020-11-15T15:41:04+00:00",
                root: {
                  id: "63298a73-9dff-46cf-b42d-9b2f01a56690",
                  nickname: "product",
                },
                seenAt: "2020-02-01T15:41:04+00:00",
                sortsRiskLevel: 80,
                sortsSuggestions: null,
              },
            },
          },
        },
      },
    ];
    const mockedToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
          first: 150,
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            toeLines: {
              __typename: "ToeLinesConnection",
              edges: [
                {
                  __typename: "ToeLinesEdge",
                  node: {
                    __typename: "ToeLines",
                    attackedAt: "2021-02-20T05:00:00+00:00",
                    attackedBy: "test2@test.com",
                    attackedLines: 4,
                    bePresent: true,
                    bePresentUntil: "",
                    comments: "comment 1",
                    filename: "test/test#.config",
                    firstAttackAt: "2020-02-19T15:41:04+00:00",
                    hasVulnerabilities: false,
                    lastAuthor: "user@gmail.com",
                    lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                    loc: 8,
                    modifiedDate: "2020-11-15T15:41:04+00:00",
                    root: {
                      id: "63298a73-9dff-46cf-b42d-9b2f01a56690",
                      nickname: "product",
                    },
                    seenAt: "2020-02-01T15:41:04+00:00",
                    sortsRiskLevel: 80,
                    sortsSuggestions: null,
                  },
                },
                {
                  __typename: "ToeLinesEdge",
                  node: {
                    __typename: "ToeLines",
                    attackedAt: "",
                    attackedBy: "test@test.com",
                    attackedLines: 120,
                    bePresent: false,
                    bePresentUntil: "2021-01-01T15:41:04+00:00",
                    comments: "comment 2",
                    filename: "test2/test.sh",
                    firstAttackAt: "",
                    hasVulnerabilities: true,
                    lastAuthor: "user@gmail.com",
                    lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
                    loc: 172,
                    modifiedDate: "2020-11-16T15:41:04+00:00",
                    root: {
                      id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                      nickname: "integrates_1",
                    },
                    seenAt: "2020-01-01T15:41:04+00:00",
                    sortsRiskLevel: 0,
                    sortsSuggestions: null,
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
      { action: "api_resolvers_toe_lines_attacked_at_resolve" },
      { action: "api_resolvers_toe_lines_attacked_by_resolve" },
      { action: "api_resolvers_toe_lines_attacked_lines_resolve" },
      { action: "api_resolvers_toe_lines_be_present_until_resolve" },
      { action: "api_resolvers_toe_lines_comments_resolve" },
      { action: "api_resolvers_toe_lines_first_attack_at_resolve" },
      { action: "api_mutations_update_toe_lines_attacked_lines_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          mocks={[mockedToeLines, ...mocksMutation]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    const newValue = 6;

    userEvent.type(screen.getAllByRole("spinbutton")[1], "{backspace}");
    userEvent.type(screen.getAllByRole("spinbutton")[1], newValue.toString());
    userEvent.type(screen.getAllByRole("spinbutton")[1], "{enter}");

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.toe.lines.alerts.verifyToeLines.success",
        "groupAlerts.updatedTitle"
      );
      expect(screen.getAllByRole("spinbutton")[1]).toHaveValue(newValue);
    });
  });
});
