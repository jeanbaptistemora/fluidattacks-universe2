import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_TOE_LANGUAGES } from "./queries";

import { GroupToeLanguagesView } from ".";

describe("groupToeLanguagesView", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupToeLanguagesView).toBe("function");
  });

  it("should display group toe languages", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedToeLanguages: MockedResponse = {
      request: {
        query: GET_TOE_LANGUAGES,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            __typename: "CodeLanguages",
            codeLanguages: [
              {
                language: "Python",
                loc: 15,
              },
              {
                language: "Ruby",
                loc: 27,
              },
            ],
            name: "unittesting",
          },
        },
      },
    };
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/languages"]}>
        <MockedProvider addTypename={true} mocks={[mockedToeLanguages]}>
          <Route path={"/:groupName/surface/languages"}>
            <GroupToeLanguagesView />
          </Route>
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
        "group.toe.codeLanguages.lang",
        "group.toe.codeLanguages.loc",
        "group.toe.codeLanguages.percent",
      ]
        .join("")
        .replace(/[^a-zA-Z ]/gu, "")
    );
    expect(screen.getAllByRole("row")[1].textContent).toStrictEqual(
      ["Python", "15", "36%"].join("")
    );
    expect(screen.getAllByRole("row")[2].textContent).toStrictEqual(
      ["Ruby", "27", "64%"].join("")
    );
  });

  it("should display empty table", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedToeLanguages: MockedResponse = {
      request: {
        query: GET_TOE_LANGUAGES,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            __typename: "CodeLanguages",
            codeLanguages: null,
            name: "unittesting",
          },
        },
      },
    };
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/languages"]}>
        <MockedProvider addTypename={true} mocks={[mockedToeLanguages]}>
          <Route path={"/:groupName/surface/languages"}>
            <GroupToeLanguagesView />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    const numberOfRows: number = 2;
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(screen.getByText("table.noDataIndication")).toBeInTheDocument();
  });
});
