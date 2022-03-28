import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GroupSettingsView } from "scenes/Dashboard/containers/GroupSettingsView";
import { GET_TAGS } from "scenes/Dashboard/containers/GroupSettingsView/queries";
import { msgError } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

describe("GroupSettingsView", (): void => {
  const mocksTags: Readonly<MockedResponse> = {
    request: {
      query: GET_TAGS,
      variables: {
        groupName: "TEST",
      },
    },
    result: {
      data: {
        group: {
          name: "TEST",
          tags: ["test"],
        },
      },
    },
  };

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_TAGS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupSettingsView).toStrictEqual("function");
  });

  it("should render tags component", (): void => {
    expect.hasAssertions();

    const { container } = render(
      <MockedProvider addTypename={false} mocks={[mocksTags]}>
        <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
          <Route
            component={GroupSettingsView}
            path={"/orgs/:organizationName/groups/:groupName/scope"}
          />
        </MemoryRouter>
      </MockedProvider>
    );

    expect(container.querySelector("#resources")).toBeInTheDocument();
  });

  it("should render a error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MockedProvider addTypename={false} mocks={mockError}>
        <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
          <Route
            component={GroupSettingsView}
            path={"/orgs/:organizationName/groups/:groupName/scope"}
          />
        </MemoryRouter>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });
    jest.clearAllMocks();
  });

  it("should render files component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MockedProvider addTypename={false} mocks={[mocksTags]}>
        <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
          <Route
            component={GroupSettingsView}
            path={"/orgs/:organizationName/groups/:groupName/scope"}
          />
        </MemoryRouter>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });
  });
});
