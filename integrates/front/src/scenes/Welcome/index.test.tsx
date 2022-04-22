import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import {
  ADD_ORGANIZATION,
  AUTOENROLL_DEMO,
  GET_NEW_ORGANIZATION_NAME,
  GET_USER_WELCOME,
} from "./queries";

import { Welcome } from ".";

describe("Welcome", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Welcome).toBe("function");
  });

  it("should render welcome menu to new users", async (): Promise<void> => {
    expect.hasAssertions();

    const getUserWelcomeMock: MockedResponse = {
      request: {
        query: GET_USER_WELCOME,
      },
      result: {
        data: {
          me: {
            organizations: [],
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
      expect(screen.getAllByRole("heading").length).toBeGreaterThan(0);

      const options = screen.getAllByRole("article");

      expect(options[0].textContent).toContain("tour");
      expect(options[1].textContent).toContain("demo");
    });
  });

  it("should render tour", async (): Promise<void> => {
    expect.hasAssertions();

    const getUserWelcomeMock: MockedResponse = {
      request: {
        query: GET_USER_WELCOME,
      },
      result: {
        data: {
          me: {
            organizations: [],
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
      userEvent.click(screen.getAllByRole("article")[0]);

      expect(screen.getByRole("textbox")).toBeInTheDocument();
      expect(screen.getAllByRole("button")).toHaveLength(2);
    });
  });

  it("should redirect after completing the tour", async (): Promise<void> => {
    expect.hasAssertions();

    const getUserWelcomeBeforeMock: MockedResponse = {
      request: {
        query: GET_USER_WELCOME,
      },
      result: {
        data: {
          me: {
            organizations: [],
            userEmail: "test@gmail.com",
          },
        },
      },
    };
    const getNewOrganizationNameMock: MockedResponse = {
      request: {
        query: GET_NEW_ORGANIZATION_NAME,
      },
      result: {
        data: {
          internalNames: {
            name: "neworg",
          },
        },
      },
    };

    const addOrganizationMock: MockedResponse = {
      request: {
        query: ADD_ORGANIZATION,
        variables: {
          name: "NEWORG",
        },
      },
      result: {
        data: {
          addOrganization: {
            organization: {
              id: "ORG#fbfb803d-3c1a-416a-af25-508028e0f608",
              name: "neworg",
            },
            success: true,
          },
        },
      },
    };
    const getUserWelcomeAfterMock: MockedResponse = {
      request: {
        query: GET_USER_WELCOME,
      },
      result: {
        data: {
          me: {
            organizations: [{ name: "neworg" }],
            userEmail: "test@gmail.com",
          },
        },
      },
    };

    render(
      <MemoryRouter initialEntries={["/welcome"]}>
        <MockedProvider
          addTypename={false}
          mocks={[
            getUserWelcomeBeforeMock,
            getNewOrganizationNameMock,
            addOrganizationMock,
            getUserWelcomeAfterMock,
          ]}
        >
          <Route component={Welcome} path={"/"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      userEvent.click(screen.getAllByRole("article")[0]);
    });

    const buttons = screen.getAllByRole("button");

    expect(buttons).toHaveLength(2);

    await waitFor((): void => {
      userEvent.click(buttons[1]);

      expect(screen.getAllByRole("list").length).toBeGreaterThan(1);
    });
  });

  it("should render dashboard when browsing demo", async (): Promise<void> => {
    expect.hasAssertions();

    const getUserWelcomeMock: MockedResponse = {
      request: {
        query: GET_USER_WELCOME,
      },
      result: {
        data: {
          me: {
            organizations: [],
            userEmail: "test@gmail.com",
          },
        },
      },
    };
    const autoenrollDemoMock: MockedResponse = {
      request: {
        query: AUTOENROLL_DEMO,
      },
      result: {
        data: {
          autoenrollDemo: {
            success: true,
          },
        },
      },
    };
    const getUserWelcomeAfterMock: MockedResponse = {
      request: {
        query: GET_USER_WELCOME,
      },
      result: {
        data: {
          me: {
            organizations: [{ name: "okada" }],
            userEmail: "test@gmail.com",
          },
        },
      },
    };

    render(
      <MemoryRouter initialEntries={["/welcome"]}>
        <MockedProvider
          addTypename={false}
          mocks={[
            getUserWelcomeMock,
            autoenrollDemoMock,
            getUserWelcomeAfterMock,
          ]}
        >
          <Route component={Welcome} path={"/"} />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      userEvent.click(screen.getAllByRole("article")[1]);
    });

    await waitFor((): void => {
      expect(screen.getAllByRole("list").length).toBeGreaterThan(1);
    });
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
