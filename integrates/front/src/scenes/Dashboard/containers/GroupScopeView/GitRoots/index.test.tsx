import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { ManagementModal } from "./ManagementModal";

import { GitRoots } from ".";
import type { IGitRootAttr } from "../types";
import { authzGroupContext, authzPermissionsContext } from "utils/authz/config";

describe("GitRoots", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GitRoots).toStrictEqual("function");
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
        credentials: {
          id: "",
          key: "",
          name: "",
          password: "",
          token: "",
          type: "",
          user: "",
        },
        environment: "",
        environmentUrls: ["https://app.fluidattacks.com"],
        gitignore: [],
        id: "",
        includesHealthCheck: false,
        nickname: "",
        secrets: [],
        state: "ACTIVE",
        url: "https://gitlab.com/fluidattacks/product",
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
      expect(screen.queryAllByRole("button")).toHaveLength(4);
    });

    expect(
      screen.queryByRole("textbox", { name: "url" })
    ).not.toBeInTheDocument();

    userEvent.click(
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

    const handleClose: jest.Mock = jest.fn();
    const handleSubmit: jest.Mock = jest.fn();
    render(
      <authzGroupContext.Provider
        value={new PureAbility([{ action: "is_continuous" }])}
      >
        <authzPermissionsContext.Provider
          value={new PureAbility([{ action: "update_git_root_filter" }])}
        >
          <MockedProvider>
            <ManagementModal
              groupName={""}
              initialValues={undefined}
              nicknames={[]}
              onClose={handleClose}
              onSubmitEnvs={handleSubmit}
              onSubmitRepo={handleSubmit}
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
      screen.queryAllByRole("checkbox", { name: "includesHealthCheckA" })
    ).toHaveLength(0);

    userEvent.click(screen.getByRole("radio", { name: "Yes" }));

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("checkbox", { name: "includesHealthCheckA" })
      ).toHaveLength(1);
    });

    userEvent.click(screen.getAllByRole("button")[2]);

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

    const handleClose: jest.Mock = jest.fn();
    const handleSubmit: jest.Mock = jest.fn();
    const initialValues: IGitRootAttr = {
      __typename: "GitRoot",
      branch: "",
      cloningStatus: {
        message: "",
        status: "UNKNOWN",
      },
      credentials: {
        id: "",
        key: "",
        name: "",
        password: "",
        token: "",
        type: "",
        user: "",
      },
      environment: "",
      environmentUrls: [""],
      gitignore: [],
      id: "",
      includesHealthCheck: false,
      nickname: "",
      secrets: [],
      state: "ACTIVE",
      url: "https://gitlab.com/fluidattacks/product",
    };
    render(
      <authzPermissionsContext.Provider
        value={
          new PureAbility([
            { action: "api_mutations_update_git_environments_mutate" },
          ])
        }
      >
        <MockedProvider>
          <ManagementModal
            groupName={""}
            initialValues={initialValues}
            nicknames={[]}
            onClose={handleClose}
            onSubmitEnvs={handleSubmit}
            onSubmitRepo={handleSubmit}
          />
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      // eslint-disable-next-line @typescript-eslint/no-magic-numbers
      expect(screen.queryAllByRole("link")).toHaveLength(3);
    });
    userEvent.click(
      screen.getByRole("link", { name: "group.scope.git.envUrls" })
    );

    await waitFor((): void => {
      expect(
        screen.getByRole("textbox", { name: "environmentUrls[0]" })
      ).toBeInTheDocument();
    });

    expect(screen.getByText("confirmmodal.proceed")).toBeDisabled();

    userEvent.type(
      screen.getByRole("textbox", { name: "environmentUrls[0]" }),
      "https://app.fluidattacks.com/"
    );
    await waitFor((): void => {
      expect(screen.getByText("confirmmodal.proceed")).not.toBeDisabled();
    });
    userEvent.click(screen.getByText("confirmmodal.proceed"));
    await waitFor((): void => {
      expect(handleSubmit).toHaveBeenCalledWith(
        {
          ...initialValues,
          environmentUrls: ["https://app.fluidattacks.com/"],
        },
        expect.anything()
      );
    });
    userEvent.click(screen.getByText("confirmmodal.cancel"));

    await waitFor((): void => {
      expect(handleClose).toHaveBeenCalledTimes(1);
    });

    jest.clearAllMocks();
  });
});
