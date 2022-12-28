import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";

import { Portfolio } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Portfolio";
import type { IPortfolioProps } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Portfolio";
import {
  ADD_GROUP_TAGS_MUTATION,
  GET_TAGS,
  REMOVE_GROUP_TAG_MUTATION,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("Portfolio", (): void => {
  const mockProps: IPortfolioProps = {
    groupName: "TEST",
  };

  const mocksTags: readonly MockedResponse[] = [
    {
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
            tags: ["test-tag1", "test-tag2"],
          },
        },
      },
    },
    {
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
            tags: ["test-tag1"],
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Portfolio).toBe("function");
  });

  it("should add a tag", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_GROUP_TAGS_MUTATION,
          variables: {
            groupName: "TEST",
            tagsData: JSON.stringify(["test-new-tag"]),
          },
        },
        result: { data: { addGroupTags: { success: true } } },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_group_tags_mutate" },
    ]);
    render(
      <MockedProvider
        addTypename={false}
        mocks={mocksTags.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Portfolio groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await screen.findByText("searchFindings.tabResources.addRepository");
    await userEvent.click(
      screen.getByText("searchFindings.tabResources.addRepository")
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "tags[0]" }),
      "test-new-tag"
    );
    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
    });
  });

  it("should remove a tag", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_GROUP_TAG_MUTATION,
          variables: {
            groupName: "TEST",
            tagToRemove: "test-tag1",
          },
        },
        result: { data: { removeGroupTag: { success: true } } },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_remove_group_tag_mutate" },
    ]);
    render(
      <MockedProvider
        addTypename={false}
        mocks={mocksTags.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Portfolio groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await screen.findByRole("row", { name: "test-tag1" });

    await userEvent.click(screen.getByRole("radio", { name: "test-tag1" }));
    await userEvent.click(
      screen.getByText("searchFindings.tabResources.removeRepository")
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "searchFindings.tabResources.successRemove",
        "searchFindings.tabUsers.titleSuccess"
      );
    });
  });

  it("should sort tags", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <MockedProvider addTypename={false} mocks={mocksTags}>
        <Portfolio groupName={mockProps.groupName} />
      </MockedProvider>
    );

    await screen.findByRole("columnheader");

    expect(screen.getAllByRole("cell")[0].textContent).toBe("test-tag1");

    await userEvent.click(
      screen.getByRole("columnheader", {
        name: "searchFindings.tabResources.tags.title",
      })
    );

    await userEvent.click(
      screen.getByRole("columnheader", {
        name: "searchFindings.tabResources.tags.title",
      })
    );

    expect(screen.getAllByRole("cell")[0].textContent).toBe("test-tag2");
  });

  it("should handle errors when add a tag", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_GROUP_TAGS_MUTATION,
          variables: {
            groupName: "TEST",
            tagsData: JSON.stringify(["test-new-tag"]),
          },
        },
        result: {
          errors: [
            new GraphQLError("Access denied"),
            new GraphQLError("Exception - One or more values already exist"),
          ],
        },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_group_tags_mutate" },
    ]);

    render(
      <MockedProvider
        addTypename={false}
        mocks={mocksTags.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Portfolio groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await screen.findByText("searchFindings.tabResources.addRepository");
    await userEvent.click(
      screen.getByText("searchFindings.tabResources.addRepository")
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "tags[0]" }),
      "test-new-tag"
    );
    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(2);
    });
  });

  it("should handle error when remove a tag", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_GROUP_TAG_MUTATION,
          variables: {
            groupName: "TEST",
            tagToRemove: "test-tag1",
          },
        },
        result: { errors: [new GraphQLError("Access denied")] },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_remove_group_tag_mutate" },
    ]);
    render(
      <MockedProvider
        addTypename={false}
        mocks={mocksTags.concat(mocksMutation)}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Portfolio groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await screen.findByRole("row", { name: "test-tag1" });

    await userEvent.click(screen.getByRole("radio", { name: "test-tag1" }));
    await userEvent.click(
      screen.getByText("searchFindings.tabResources.removeRepository")
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(1);
    });
  });

  it("should handle error when there are repeated tags", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_group_tags_mutate" },
    ]);
    render(
      <MockedProvider addTypename={false} mocks={mocksTags}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Portfolio groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await screen.findByText("searchFindings.tabResources.addRepository");
    await userEvent.click(
      screen.getByText("searchFindings.tabResources.addRepository")
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "tags[0]" }),
      "test-tag1"
    );
    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "searchFindings.tabResources.repeatedItem"
      );
    });
  });
});
