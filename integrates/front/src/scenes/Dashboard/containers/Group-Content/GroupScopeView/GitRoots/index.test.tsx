import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { ManagementModal } from "./ManagementModal";

import { GitRoots } from ".";
import type { IFormValues, IGitRootAttr } from "../types";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";

describe("GitRoots", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GitRoots).toBe("function");
  });

  it("should render tables", async (): Promise<void> => {
    expect.hasAssertions();

    const roots: IGitRootAttr[] = [
      {
        __typename: "GitRoot",
        branch: "",
        cloningStatus: {
          message: "",
          status: "UNKNOWN",
        },
        createdAt: new Date("2022-02-10T14:58:10+00:00"),
        createdBy: "testuser1@test.test",
        credentials: {
          auth: "",
          azureOrganization: "",
          id: "",
          isPat: false,
          key: "",
          name: "",
          password: "",
          token: "",
          type: "",
          typeCredential: "",
          user: "",
        },
        environment: "",
        gitEnvironmentUrls: [
          {
            cloudName: undefined,
            createdAt: new Date("2022-04-27T17:30:07.230355"),
            createdBy: null,
            id: "3f6eb6274ec7dc2855451c0fbb4ff9485360be5b",
            secrets: [],
            url: "https://app.fluidattacks.com",
            urlType: "URL",
          },
        ],
        gitignore: [],
        healthCheckConfirm: [],
        id: "",
        includesHealthCheck: false,
        lastEditedAt: new Date("2022-10-21T15:58:31+00:00"),
        lastEditedBy: "testuser2@test.test",
        nickname: "",
        secrets: [],
        state: "ACTIVE",
        url: "https://gitlab.com/fluidattacks/universe",
        useVpn: false,
      },
    ];
    const refetch: jest.Mock = jest.fn();
    render(
      <MockedProvider>
        <MemoryRouter initialEntries={["/TEST"]}>
          <GitRoots
            groupName={"unittesting"}
            onUpdate={refetch}
            roots={roots}
          />
        </MemoryRouter>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(2);
    });
  });

  it("should render action buttons", async (): Promise<void> => {
    expect.hasAssertions();

    const refetch: jest.Mock = jest.fn();
    render(
      <MockedProvider>
        <MemoryRouter initialEntries={["/TEST"]}>
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "api_mutations_add_git_root_mutate" },
                { action: "api_mutations_update_git_root_mutate" },
              ])
            }
          >
            <GitRoots groupName={"unittesting"} onUpdate={refetch} roots={[]} />
          </authzPermissionsContext.Provider>
        </MemoryRouter>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(5);
    });

    expect(
      screen.queryByRole("textbox", { name: "url" })
    ).not.toBeInTheDocument();

    await userEvent.click(
      screen.getByRole("button", { name: "group.scope.common.add" })
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "url" })
      ).toBeInTheDocument();
    });
    jest.clearAllMocks();
  });

  it("should render git modal", async (): Promise<void> => {
    expect.hasAssertions();

    const finishTour: jest.Mock = jest.fn();
    const handleClose: jest.Mock = jest.fn();
    const handleSubmit: jest.Mock = jest.fn();
    render(
      <authzGroupContext.Provider
        value={new PureAbility([{ action: "has_squad" }])}
      >
        <authzPermissionsContext.Provider
          value={
            new PureAbility([
              { action: "update_git_root_filter" },
              { action: "api_mutations_add_secret_mutate" },
              { action: "api_mutations_update_git_root_mutate" },
            ])
          }
        >
          <MockedProvider>
            <ManagementModal
              finishTour={finishTour}
              groupName={""}
              initialValues={undefined}
              isEditing={false}
              manyRows={false}
              modalMessages={{ message: "", type: "success" }}
              nicknames={["universe"]}
              onClose={handleClose}
              onSubmitRepo={handleSubmit}
              runTour={false}
            />
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </authzGroupContext.Provider>
    );

    // Repository fields
    await waitFor((): void => {
      expect(screen.getByRole("textbox", { name: "url" })).toBeInTheDocument();
    });

    expect(screen.getByRole("textbox", { name: "branch" })).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: "environment" })
    ).toBeInTheDocument();

    // Health Check
    expect(
      screen.queryAllByRole("checkbox", { name: "healthCheckConfirm" })
    ).toHaveLength(0);

    // Present just if duplicated when adding
    expect(
      screen.queryByRole("textbox", { name: "nickname" })
    ).not.toBeInTheDocument();

    await userEvent.clear(screen.getByRole("textbox", { name: "url" }));
    await userEvent.type(
      screen.getByRole("textbox", { name: "url" }),
      "https://gitlab.com/fluidattacks/universe"
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "nickname" })
      ).toBeInTheDocument();
    });

    await userEvent.click(screen.getByRole("radio", { name: "Yes" }));

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("checkbox", { name: "healthCheckConfirm" })
      ).toHaveLength(1);
    });

    await userEvent.click(screen.getAllByRole("button")[3]);

    // Filters
    await waitFor((): void => {
      expect(
        screen.getByRole("textbox", { name: "gitignore[0]" })
      ).toBeInTheDocument();
    });

    jest.clearAllMocks();
  });

  it("should render envs modal", async (): Promise<void> => {
    expect.hasAssertions();

    const finishTour: jest.Mock = jest.fn();
    const handleClose: jest.Mock = jest.fn();
    const handleSubmit: jest.Mock = jest.fn();
    const initialValues: IFormValues = {
      branch: "",
      cloningStatus: {
        message: "",
        status: "UNKNOWN",
      },
      credentials: {
        auth: "",
        azureOrganization: "",
        id: "",
        isPat: false,
        key: "",
        name: "",
        password: "",
        token: "",
        type: "",
        typeCredential: "",
        user: "",
      },
      environment: "",
      environmentUrls: [],
      gitEnvironmentUrls: [
        {
          cloudName: undefined,
          createdAt: new Date("2022-04-27T17:30:07.230355"),
          createdBy: "user_test@test.test",
          id: "adc83b19e793491b1c6ea0fd8b46cd9f32e592fc",
          secrets: [],
          url: "",
          urlType: "URL",
        },
      ],
      gitignore: [],
      healthCheckConfirm: [],
      id: "",
      includesHealthCheck: false,
      nickname: "",
      secrets: [],
      state: "ACTIVE",
      url: "https://gitlab.com/fluidattacks/universe",
      useVpn: false,
    };
    render(
      <authzPermissionsContext.Provider
        value={
          new PureAbility([
            { action: "api_mutations_update_git_environments_mutate" },
            { action: "api_mutations_add_secret_mutate" },
            { action: "api_mutations_update_git_root_mutate" },
            { action: "api_resolvers_git_root_secrets_resolve" },
          ])
        }
      >
        <MockedProvider>
          <ManagementModal
            finishTour={finishTour}
            groupName={""}
            initialValues={initialValues}
            isEditing={true}
            manyRows={false}
            modalMessages={{ message: "", type: "success" }}
            nicknames={[]}
            onClose={handleClose}
            onSubmitRepo={handleSubmit}
            runTour={false}
          />
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );

    // Repository fields
    await waitFor((): void => {
      expect(screen.getByRole("textbox", { name: "url" })).toBeInTheDocument();
    });

    expect(screen.getByRole("textbox", { name: "url" })).toHaveValue(
      "https://gitlab.com/fluidattacks/universe"
    );
    // Present always when editing
    expect(
      screen.queryByRole("textbox", { name: "nickname" })
    ).toBeInTheDocument();

    await waitFor((): void => {
      // eslint-disable-next-line @typescript-eslint/no-magic-numbers
      expect(screen.queryAllByRole("link")).toHaveLength(3);
    });

    jest.clearAllMocks();
  });
});
