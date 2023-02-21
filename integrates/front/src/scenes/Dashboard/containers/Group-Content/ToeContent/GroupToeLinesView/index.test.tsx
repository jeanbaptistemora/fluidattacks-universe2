import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_TOE_LINES, VERIFY_TOE_LINES } from "./queries";

import { GroupToeLinesView } from ".";
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

describe("groupToeLinesView", (): void => {
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
          codeLanguages: null,
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
                    nickname: "universe",
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
            total: 2,
          },
        },
      },
    },
  };

  const mockedPermissions = new PureAbility<string>([
    { action: "api_resolvers_toe_lines_attacked_at_resolve" },
    { action: "api_resolvers_toe_lines_attacked_by_resolve" },
    { action: "api_resolvers_toe_lines_attacked_lines_resolve" },
    { action: "api_resolvers_toe_lines_be_present_until_resolve" },
    { action: "api_resolvers_toe_lines_comments_resolve" },
    { action: "api_resolvers_toe_lines_first_attack_at_resolve" },
    { action: "see_toe_lines_coverage" },
  ]);

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupToeLinesView).toBe("function");
  });

  it("should display group toe lines", async (): Promise<void> => {
    expect.hasAssertions();

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

    expect(
      screen.getAllByRole("row")[0].textContent?.replace(/[^a-zA-Z ]/gu, "")
    ).toStrictEqual(
      [
        "group.toe.lines.root",
        "group.toe.lines.loc",
        "group.toe.lines.status",
        "group.toe.lines.modifiedDate",
        "group.toe.lines.lastCommit",
        "group.toe.lines.coverage",
        "group.toe.lines.attackedLines",
        "group.toe.lines.attackedAt",
        "group.toe.lines.comments",
      ]
        .join("")
        .replace(/[^a-zA-Z ]/gu, "")
    );
    expect(screen.getAllByRole("row")[2].textContent).toStrictEqual(
      [
        "integrates_1",
        "172",
        "Group.toe.lines.vulnerable",
        "2020-11-16",
        "f9e4beb",
        "70%",
        "120",
        "",
        "comment 2",
      ].join("")
    );
    expect(screen.getAllByRole("row")[1].textContent).toStrictEqual(
      [
        "universe",
        "8",
        "Group.toe.lines.safe",
        "2020-11-15",
        "f9e4beb",
        "50%",
        "4",
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
    const handleMockedPermissions = new PureAbility<string>([
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
          <authzPermissionsContext.Provider value={handleMockedPermissions}>
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

    expect(
      screen.getByText("group.toe.lines.actionButtons.verifyButton.text")
    ).toBeDisabled();

    await userEvent.click(screen.getAllByRole("checkbox")[1]);
    await userEvent.click(screen.getAllByRole("checkbox")[2]);

    expect(
      screen.getByText("group.toe.lines.actionButtons.verifyButton.text")
    ).not.toBeDisabled();

    await userEvent.click(
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
                  nickname: "universe",
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
    const handleMockedPermissions = new PureAbility<string>([
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
          <authzPermissionsContext.Provider value={handleMockedPermissions}>
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

    await userEvent.type(screen.getAllByRole("spinbutton")[0], "{backspace}");
    await userEvent.type(
      screen.getAllByRole("spinbutton")[0],
      newValue.toString()
    );
    await userEvent.type(screen.getAllByRole("spinbutton")[0], "{enter}");

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.toe.lines.alerts.verifyToeLines.success",
        "groupAlerts.updatedTitle"
      );
      expect(screen.getAllByRole("spinbutton")[0]).toHaveValue(newValue);
    });
  });

  it("should have filters", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

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

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    expect(
      screen.getByRole("textbox", { name: "filename" })
    ).toBeInTheDocument();
    expect(screen.getAllByRole("spinbutton", { name: "loc" })).toHaveLength(2);
    expect(
      screen.getByRole("combobox", { name: "hasVulnerabilities" })
    ).toBeInTheDocument();
    expect(
      document.querySelectorAll(`input[name="modifiedDate"]`)
    ).toHaveLength(2);
    expect(
      screen.getByRole("textbox", { name: "lastCommit" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: "lastAuthor" })
    ).toBeInTheDocument();
    expect(document.querySelectorAll(`input[name="seenAt"]`)).toHaveLength(2);
    expect(
      screen.getAllByRole("spinbutton", { name: "sortsRiskLevel" })
    ).toHaveLength(2);
    expect(
      screen.getByRole("combobox", { name: "bePresent" })
    ).toBeInTheDocument();
    expect(
      screen.getAllByRole("spinbutton", { name: "attackedLines" })
    ).toHaveLength(2);
    expect(document.querySelectorAll(`input[name="attackedAt"]`)).toHaveLength(
      2
    );
    expect(
      screen.getByRole("textbox", { name: "attackedBy" })
    ).toBeInTheDocument();
    expect(
      document.querySelectorAll(`input[name="firstAttackAt"]`)
    ).toHaveLength(2);
    expect(
      screen.getByRole("textbox", { name: "comments" })
    ).toBeInTheDocument();
    expect(
      document.querySelectorAll(`input[name="bePresentUntil"]`)
    ).toHaveLength(2);
  });

  it("should filter by filename", async (): Promise<void> => {
    expect.hasAssertions();

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

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(screen.getByRole("textbox", { name: "filename" }), {
      target: { value: "test/test#.config" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by loc", async (): Promise<void> => {
    expect.hasAssertions();

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

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(screen.getAllByRole("spinbutton", { name: "loc" })[0], {
      target: { value: 170 },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by modified date", async (): Promise<void> => {
    expect.hasAssertions();

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

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(
      document.querySelectorAll(`input[name="modifiedDate"]`)[0],
      {
        target: { value: "2020-11-16" },
      }
    );
    fireEvent.change(
      document.querySelectorAll(`input[name="modifiedDate"]`)[1],
      {
        target: { value: "2022-11-17" },
      }
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by last commit", async (): Promise<void> => {
    expect.hasAssertions();

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

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(screen.getByRole("textbox", { name: "lastCommit" }), {
      target: { value: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });
});
