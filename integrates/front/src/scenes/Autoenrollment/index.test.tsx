/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { FetchMockStatic } from "fetch-mock";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { GET_STAKEHOLDER_GROUPS, VALIDATE_GIT_ACCESS } from "./queries";
import type {
  ICheckGitAccessResult,
  IGetStakeholderGroupsResult,
} from "./types";
import { EMAIL_DOMAINS_URL } from "./utils";

import { Autoenrollment } from ".";
import { getCache } from "utils/apollo";
import { COUNTRIES_URL } from "utils/countries";

describe("Autoenrollment", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Autoenrollment).toBe("function");
  });

  it("should validate with HTTPS access token", async (): Promise<void> => {
    expect.hasAssertions();

    const variables = {
      branch: "main",
      credentials: {
        key: undefined,
        name: "test-creds",
        password: "",
        token: "test-token",
        type: "HTTPS",
        user: "",
      },
      url: "https://gitlab.com/fluidattacks/universe",
    };
    const groupsMock: MockedResponse<IGetStakeholderGroupsResult> = {
      request: {
        query: GET_STAKEHOLDER_GROUPS,
      },
      result: {
        data: {
          me: {
            organizations: [],
            userEmail: "jdoe@fluidattacks.com",
          },
        },
      },
    };
    const accessMock: MockedResponse<ICheckGitAccessResult> = {
      request: {
        query: VALIDATE_GIT_ACCESS,
        variables,
      },
      result: {
        data: {
          validateGitAccess: { success: true },
        },
      },
    };

    const mockedFetch = fetch as FetchMockStatic & typeof fetch;
    mockedFetch.mock(EMAIL_DOMAINS_URL, { status: 200, text: "" });
    mockedFetch.mock(COUNTRIES_URL, { body: "[]", status: 200 });

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider cache={getCache()} mocks={[groupsMock, accessMock]}>
          <Autoenrollment />
        </MockedProvider>
      </MemoryRouter>
    );

    const urlInput = await screen.findByRole("textbox", { name: "url" });
    userEvent.type(urlInput, variables.url);

    const branchInput = await screen.findByRole("textbox", { name: "branch" });
    userEvent.type(branchInput, variables.branch);

    const credentialsTypeSelect = await screen.findByRole("combobox", {
      name: "credentials.type",
    });
    userEvent.selectOptions(credentialsTypeSelect, [
      variables.credentials.type,
    ]);

    const credentialsNameInput = await screen.findByRole("textbox", {
      name: "credentials.name",
    });
    userEvent.type(credentialsNameInput, variables.credentials.name);

    const credentialsAuthSelect = await screen.findByRole("combobox", {
      name: "credentials.auth",
    });
    userEvent.selectOptions(credentialsAuthSelect, ["TOKEN"]);

    const credentialsTokenInput = await screen.findByRole("textbox", {
      name: "credentials.token",
    });
    userEvent.type(credentialsTokenInput, variables.credentials.token);

    const environmentInput = await screen.findByRole("textbox", {
      name: "env",
    });
    userEvent.type(environmentInput, "production");

    const submitButton = await screen.findByText("autoenrollment.next");
    userEvent.click(submitButton);

    await expect(
      screen.findByText("autoenrollment.step2")
    ).resolves.toBeInTheDocument();

    mockedFetch.reset();
  });

  it("should validate with HTTPS user", async (): Promise<void> => {
    expect.hasAssertions();

    const variables = {
      branch: "main",
      credentials: {
        key: undefined,
        name: "test-creds",
        password: "test-password",
        token: "",
        type: "HTTPS",
        user: "test-user",
      },
      url: "https://gitlab.com/fluidattacks/universe",
    };
    const groupsMock: MockedResponse<IGetStakeholderGroupsResult> = {
      request: {
        query: GET_STAKEHOLDER_GROUPS,
      },
      result: {
        data: {
          me: {
            organizations: [],
            userEmail: "jdoe@fluidattacks.com",
          },
        },
      },
    };
    const accessMock: MockedResponse<ICheckGitAccessResult> = {
      request: {
        query: VALIDATE_GIT_ACCESS,
        variables,
      },
      result: {
        data: {
          validateGitAccess: { success: true },
        },
      },
    };

    const mockedFetch = fetch as FetchMockStatic & typeof fetch;
    mockedFetch.mock(EMAIL_DOMAINS_URL, { status: 200, text: "" });
    mockedFetch.mock(COUNTRIES_URL, { body: "[]", status: 200 });

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider cache={getCache()} mocks={[groupsMock, accessMock]}>
          <Autoenrollment />
        </MockedProvider>
      </MemoryRouter>
    );

    const urlInput = await screen.findByRole("textbox", { name: "url" });
    userEvent.type(urlInput, variables.url);

    const branchInput = await screen.findByRole("textbox", { name: "branch" });
    userEvent.type(branchInput, variables.branch);

    const credentialsTypeSelect = await screen.findByRole("combobox", {
      name: "credentials.type",
    });
    userEvent.selectOptions(credentialsTypeSelect, [
      variables.credentials.type,
    ]);

    const credentialsNameInput = await screen.findByRole("textbox", {
      name: "credentials.name",
    });
    userEvent.type(credentialsNameInput, variables.credentials.name);

    const credentialsAuthSelect = await screen.findByRole("combobox", {
      name: "credentials.auth",
    });
    userEvent.selectOptions(credentialsAuthSelect, ["USER"]);

    const credentialsUserInput = await screen.findByRole("textbox", {
      name: "credentials.user",
    });
    userEvent.type(credentialsUserInput, variables.credentials.user);

    const credentialsPasswordInput = await screen.findByLabelText(
      "autoenrollment.credentials.password"
    );
    userEvent.type(credentialsPasswordInput, variables.credentials.password);

    const environmentInput = await screen.findByRole("textbox", {
      name: "env",
    });
    userEvent.type(environmentInput, "production");

    const submitButton = await screen.findByText("autoenrollment.next");
    userEvent.click(submitButton);

    await expect(
      screen.findByText("autoenrollment.step2")
    ).resolves.toBeInTheDocument();

    mockedFetch.reset();
  });

  it("should validate with SSH", async (): Promise<void> => {
    expect.hasAssertions();

    const variables = {
      branch: "main",
      credentials: {
        key: "LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KdGVzdAotLS0tLUVORCBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0=",
        name: "test-creds",
        password: "",
        token: "",
        type: "SSH",
        user: "",
      },
      url: "https://gitlab.com/fluidattacks/universe",
    };
    const groupsMock: MockedResponse<IGetStakeholderGroupsResult> = {
      request: {
        query: GET_STAKEHOLDER_GROUPS,
      },
      result: {
        data: {
          me: {
            organizations: [],
            userEmail: "jdoe@fluidattacks.com",
          },
        },
      },
    };
    const accessMock: MockedResponse<ICheckGitAccessResult> = {
      request: {
        query: VALIDATE_GIT_ACCESS,
        variables,
      },
      result: {
        data: {
          validateGitAccess: { success: true },
        },
      },
    };

    const mockedFetch = fetch as FetchMockStatic & typeof fetch;
    mockedFetch.mock(EMAIL_DOMAINS_URL, { status: 200, text: "" });
    mockedFetch.mock(COUNTRIES_URL, { body: "[]", status: 200 });

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider cache={getCache()} mocks={[groupsMock, accessMock]}>
          <Autoenrollment />
        </MockedProvider>
      </MemoryRouter>
    );

    const urlInput = await screen.findByRole("textbox", { name: "url" });
    userEvent.type(urlInput, variables.url);

    const branchInput = await screen.findByRole("textbox", { name: "branch" });
    userEvent.type(branchInput, variables.branch);

    const credentialsTypeSelect = await screen.findByRole("combobox", {
      name: "credentials.type",
    });
    userEvent.selectOptions(credentialsTypeSelect, [
      variables.credentials.type,
    ]);

    const credentialsNameInput = await screen.findByRole("textbox", {
      name: "credentials.name",
    });
    userEvent.type(credentialsNameInput, variables.credentials.name);

    const credentialsKeyInput = await screen.findByRole("textbox", {
      name: "credentials.key",
    });
    userEvent.type(
      credentialsKeyInput,
      "-----BEGIN OPENSSH PRIVATE KEY-----\ntest\n-----END OPENSSH PRIVATE KEY-----"
    );

    const environmentInput = await screen.findByRole("textbox", {
      name: "env",
    });
    userEvent.type(environmentInput, "production");

    const submitButton = await screen.findByText("autoenrollment.next");
    userEvent.click(submitButton);

    await expect(
      screen.findByText("autoenrollment.step2")
    ).resolves.toBeInTheDocument();

    mockedFetch.reset();
  });
});
