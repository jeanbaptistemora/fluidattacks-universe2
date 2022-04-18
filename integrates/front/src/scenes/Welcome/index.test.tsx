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
    expect(typeof Welcome).toStrictEqual("function");
  });

  it("should render welcome menu", async (): Promise<void> => {
    expect.hasAssertions();

    const getUserWelcomeMock: MockedResponse = {
      request: {
        query: GET_USER_WELCOME,
      },
      result: {
        data: {
          me: {
            organizations: [{ name: "imamura" }],
            userEmail: "test@gmail.com",
          },
        },
      },
    };

    render(
      <MemoryRouter initialEntries={["/welcome"]}>
        <MockedProvider addTypename={true} mocks={[getUserWelcomeMock]}>
          <Route component={Welcome} path={"/"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.getAllByRole("heading").length).toBeGreaterThan(0);

      const options = screen.getAllByRole("article");

      expect(options[0].textContent).toContain("tour");
      expect(options[1].textContent).toContain("demo");
    });
  });
});
