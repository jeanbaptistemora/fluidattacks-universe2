import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { useTranslation } from "react-i18next";

import { Portfolio } from "scenes/Dashboard/containers/GroupSettingsView/Portfolio";
import type { IPortfolioProps } from "scenes/Dashboard/containers/GroupSettingsView/Portfolio";
import {
  ADD_GROUP_TAGS_MUTATION,
  GET_TAGS,
  REMOVE_GROUP_TAG_MUTATION,
} from "scenes/Dashboard/containers/GroupSettingsView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

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
    expect(typeof Portfolio).toStrictEqual("function");
  });

  it("should add a tag", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const { t } = useTranslation();

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
    const mockedPermissions: PureAbility<string> = new PureAbility([
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

    await screen.findByText(
      t("searchFindings.tabResources.addRepository").toString()
    );
    userEvent.click(
      screen.getByText(
        t("searchFindings.tabResources.addRepository").toString()
      )
    );
    userEvent.type(screen.getByRole("textbox"), "test-new-tag");
    userEvent.click(screen.getByText(t("confirmmodal.proceed").toString()));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
    });
  });

  it("should remove a tag", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const { t } = useTranslation();
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
    const mockedPermissions: PureAbility<string> = new PureAbility([
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

    userEvent.click(screen.getByRole("row", { name: "test-tag1" }));
    userEvent.click(
      screen.getByText(
        t("searchFindings.tabResources.removeRepository").toString()
      )
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        t("searchFindings.tabResources.successRemove"),
        t("searchFindings.tabUsers.titleSuccess")
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

    userEvent.click(screen.getByRole("columnheader"));

    expect(screen.getAllByRole("cell")[0].textContent).toBe("test-tag2");
  });

  it("should handle errors when add a tag", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const { t } = useTranslation();
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
    const mockedPermissions: PureAbility<string> = new PureAbility([
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
    await screen.findByText(
      t("searchFindings.tabResources.addRepository").toString()
    );
    userEvent.click(
      screen.getByText(
        t("searchFindings.tabResources.addRepository").toString()
      )
    );
    userEvent.type(screen.getByRole("textbox"), "test-new-tag");
    userEvent.click(screen.getByText(t("confirmmodal.proceed").toString()));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(2);
    });
  });

  it("should handle error when remove a tag", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const { t } = useTranslation();
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
    const mockedPermissions: PureAbility<string> = new PureAbility([
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

    userEvent.click(screen.getByRole("row", { name: "test-tag1" }));
    userEvent.click(
      screen.getByText(
        t("searchFindings.tabResources.removeRepository").toString()
      )
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(1);
    });
  });

  it("should handle error when there are repeated tags", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const { t } = useTranslation();
    const mockedPermissions: PureAbility<string> = new PureAbility([
      { action: "api_mutations_add_group_tags_mutate" },
    ]);
    render(
      <MockedProvider addTypename={false} mocks={mocksTags}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <Portfolio groupName={mockProps.groupName} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await screen.findByText(
      t("searchFindings.tabResources.addRepository").toString()
    );
    userEvent.click(
      screen.getByText(
        t("searchFindings.tabResources.addRepository").toString()
      )
    );
    userEvent.type(screen.getByRole("textbox"), "test-tag1");
    userEvent.click(screen.getByText(t("confirmmodal.proceed").toString()));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        t("searchFindings.tabResources.repeatedItem")
      );
    });
  });
});
