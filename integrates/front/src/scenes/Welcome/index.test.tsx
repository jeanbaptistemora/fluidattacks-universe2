import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_USER_WELCOME } from "./queries";

import { Welcome } from ".";

describe("Welcome", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Welcome).toBe("function");
  });

  it("should render dashboard to old users", async (): Promise<void> => {
    expect.hasAssertions();

    const getUserWelcomeMock: MockedResponse = {
      request: {
        query: GET_USER_WELCOME,
      },
      result: {
        data: {
          me: {
            organizations: [{ name: "another" }],
            userEmail: "test@gmail.com",
          },
        },
      },
    };

    render(
      <MemoryRouter initialEntries={["/welcome"]}>
        <MockedProvider addTypename={false} mocks={[getUserWelcomeMock]}>
          <Route component={Welcome} path={"/"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.getAllByRole("list").length).toBeGreaterThan(1);
    });
  });
});
