import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { UPDATE_TOE_LINES_ATTACKED_LINES } from "./queries";

import { HandleEditionModal } from ".";
import type { IToeLinesData } from "../types";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("handle toe lines edition modal", (): void => {
  it("should handle attacked lines edition", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UPDATE_TOE_LINES_ATTACKED_LINES,
          variables: {
            attackedLines: 5,
            comments: "This is a test of updating toe lines",
            filename: "test/test#.config",
            groupName: "groupname",
            rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
          },
        },
        result: { data: { updateToeLinesAttackedLines: { success: true } } },
      },
    ];
    const mokedToeLines: IToeLinesData[] = [
      {
        attackedAt: new Date("2021-02-20T05:00:00+00:00"),
        attackedBy: "test2@test.com",
        attackedLines: 4,
        bePresent: true,
        bePresentUntil: undefined,
        comments: "comment 1",
        coverage: 0.1,
        daysToAttack: 4,
        extension: "config",
        filename: "test/test#.config",
        firstAttackAt: new Date("2020-02-19T15:41:04+00:00"),
        hasVulnerabilities: true,
        lastAuthor: "user@gmail.com",
        lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
        loc: 8,
        modifiedDate: new Date("2020-11-15T15:41:04+00:00"),
        root: {
          id: "63298a73-9dff-46cf-b42d-9b2f01a56690",
          nickname: "universe",
        },
        rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
        rootNickname: "universe",
        seenAt: new Date("2020-02-01T15:41:04+00:00"),
        sortsRiskLevel: 80,
        sortsSuggestions: null,
      },
    ];
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={false}
          mocks={[...mocksMutation, ...mocksMutation, ...mocksMutation]}
        >
          <Route path={"/:groupName/surface/lines"}>
            <HandleEditionModal
              groupName={"groupname"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              selectedToeLinesDatas={mokedToeLines}
              setSelectedToeLinesDatas={jest.fn()}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await userEvent.clear(screen.getByRole("spinbutton"));
    await userEvent.type(screen.getByRole("spinbutton"), "5");
    await userEvent.type(
      screen.getByRole("textbox"),
      "This is a test of updating toe lines"
    );

    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(handleRefetchData).toHaveBeenCalledTimes(1);
    });

    expect(handleCloseModal).toHaveBeenCalledTimes(1);
    expect(msgSuccess).toHaveBeenCalledWith(
      "group.toe.lines.editModal.alerts.success",
      "groupAlerts.updatedTitle"
    );
  });

  it("should handle error attacked lines edition", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UPDATE_TOE_LINES_ATTACKED_LINES,
          variables: {
            attackedLines: 6,
            comments: "This is a test of error in updating toe lines",
            filename: "test/test#.config",
            groupName: "groupname",
            rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - The attacked lines must be between 0 and the loc (lines of code)"
            ),
          ],
        },
      },
    ];
    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: UPDATE_TOE_LINES_ATTACKED_LINES,
          variables: {
            attackedLines: 9,
            comments: "This is a second test of error in updating toe lines",
            filename: "test/test#.config",
            groupName: "groupname",
            rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - The attacked lines must be between 0 and the loc (lines of code)"
            ),
          ],
        },
      },
    ];
    const mokedToeLines: IToeLinesData[] = [
      {
        attackedAt: new Date("2021-02-20T05:00:00+00:00"),
        attackedBy: "test2@test.com",
        attackedLines: 4,
        bePresent: true,
        bePresentUntil: undefined,
        comments: "comment 1",
        coverage: 0.1,
        daysToAttack: 4,
        extension: "config",
        filename: "test/test#.config",
        firstAttackAt: new Date("2020-02-19T15:41:04+00:00"),
        hasVulnerabilities: true,
        lastAuthor: "user@gmail.com",
        lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
        loc: 8,
        modifiedDate: new Date("2020-11-15T15:41:04+00:00"),
        root: {
          id: "63298a73-9dff-46cf-b42d-9b2f01a56690",
          nickname: "universe",
        },
        rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
        rootNickname: "universe",
        seenAt: new Date("2020-02-01T15:41:04+00:00"),
        sortsRiskLevel: 80,
        sortsSuggestions: null,
      },
    ];
    const { rerender } = render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={false}
          mocks={[...mocksMutation, ...mocksMutation, ...mocksMutation]}
        >
          <Route path={"/:groupName/surface/lines"}>
            <HandleEditionModal
              groupName={"groupname"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              selectedToeLinesDatas={mokedToeLines}
              setSelectedToeLinesDatas={jest.fn()}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await userEvent.clear(screen.getByRole("spinbutton"));
    await userEvent.type(screen.getByRole("spinbutton"), "6");

    await userEvent.type(
      screen.getByRole("textbox"),
      "This is a test of error in updating toe lines"
    );

    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "group.toe.lines.editModal.alerts.invalidAttackedLines"
      );
    });

    rerender(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={false}
          mocks={[...mockedQueries, ...mockedQueries, ...mockedQueries]}
        >
          <Route path={"/:groupName/surface/lines"}>
            <HandleEditionModal
              groupName={"groupname"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              selectedToeLinesDatas={mokedToeLines}
              setSelectedToeLinesDatas={jest.fn()}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await userEvent.clear(screen.getByRole("spinbutton"));
    await userEvent.type(screen.getByRole("spinbutton"), "9");

    await userEvent.clear(screen.getByRole("textbox"));
    await userEvent.type(
      screen.getByRole("textbox"),
      "This is a second test of error in updating toe lines"
    );

    await userEvent.click(screen.getByText("components.modal.confirm"));

    expect(
      screen.getByText("This value must be between 0 and 8")
    ).toBeInTheDocument();
  });
});
