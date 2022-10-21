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

import {
  ADD_GIT_ROOT,
  ADD_GROUP,
  ADD_ORGANIZATION,
  GET_STAKEHOLDER_GROUPS,
  VALIDATE_GIT_ACCESS,
} from "./queries";
import type {
  IAddGitRootResult,
  IAddGroupResult,
  IAddOrganizationResult,
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

  it("should render corporate only", async (): Promise<void> => {
    expect.hasAssertions();

    const groupsMock: MockedResponse<IGetStakeholderGroupsResult> = {
      request: {
        query: GET_STAKEHOLDER_GROUPS,
      },
      result: {
        data: {
          me: {
            organizations: [],
            userEmail: "jdoe@personal.com",
          },
        },
      },
    };

    const mockedFetch = fetch as FetchMockStatic & typeof fetch;
    mockedFetch.mock(EMAIL_DOMAINS_URL, { body: "personal.com", status: 200 });
    mockedFetch.mock(COUNTRIES_URL, { body: "[]", status: 200 });

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider cache={getCache()} mocks={[groupsMock]}>
          <Autoenrollment />
        </MockedProvider>
      </MemoryRouter>
    );

    await expect(
      screen.findByText("autoenrollment.corporateOnly")
    ).resolves.toBeInTheDocument();

    mockedFetch.reset();
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

  it("should submit", async (): Promise<void> => {
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
    const orgMock: MockedResponse<IAddOrganizationResult> = {
      request: {
        query: ADD_ORGANIZATION,
        variables: {
          country: "Colombia",
          name: "TESTORG",
        },
      },
      result: {
        data: {
          addOrganization: {
            organization: {
              id: "95a104d1-3e5e-4427-afe2-b1cdcd02c5d2",
              name: "TESTORG",
            },
            success: true,
          },
        },
      },
    };
    const groupMock: MockedResponse<IAddGroupResult> = {
      request: {
        query: ADD_GROUP,
        variables: {
          description: "test description",
          groupName: "TESTGROUP",
          hasMachine: true,
          hasSquad: false,
          language: "EN",
          organizationName: "testOrg",
          service: "WHITE",
          subscription: "CONTINUOUS",
        },
      },
      result: {
        data: {
          addGroup: { success: true },
        },
      },
    };
    const rootMock: MockedResponse<IAddGitRootResult> = {
      request: {
        query: ADD_GIT_ROOT,
        variables: {
          branch: "main",
          credentials: {
            key: variables.credentials.key,
            name: variables.credentials.name,
            password: variables.credentials.password,
            token: variables.credentials.token,
            type: variables.credentials.type,
            user: variables.credentials.user,
          },
          environment: "production",
          gitignore: [],
          groupName: "TESTGROUP",
          includesHealthCheck: false,
          nickname: "",
          url: variables.url,
          useVpn: false,
        },
      },
      result: {
        data: {
          addGitRoot: { success: true },
        },
      },
    };

    const mockedFetch = fetch as FetchMockStatic & typeof fetch;
    mockedFetch.mock(EMAIL_DOMAINS_URL, { status: 200, text: "" });
    mockedFetch.mock(COUNTRIES_URL, {
      body: [{ id: 48, name: "Colombia" }],
      status: 200,
    });

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[groupsMock, accessMock, orgMock, groupMock, rootMock]}
        >
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

    const nextButton = await screen.findByText("autoenrollment.next");
    userEvent.click(nextButton);

    const orgNameInput = await screen.findByRole("textbox", {
      name: "organizationName",
    });
    userEvent.type(orgNameInput, "testOrg");

    const groupNameInput = await screen.findByRole("textbox", {
      name: "groupName",
    });
    userEvent.type(groupNameInput, "testGroup");

    const countrySelect = await screen.findByRole("combobox", {
      name: "organizationCountry",
    });
    userEvent.selectOptions(countrySelect, ["Colombia"]);

    const languageSelect = await screen.findByRole("combobox", {
      name: "reportLanguage",
    });
    userEvent.selectOptions(languageSelect, ["EN"]);

    const groupDescriptionInput = await screen.findByRole("textbox", {
      name: "groupDescription",
    });
    userEvent.type(groupDescriptionInput, "test description");

    const startTrialButton = await screen.findByText("autoenrollment.proceed");
    userEvent.click(startTrialButton);

    await expect(
      screen.findByText("autoenrollment.standby.title")
    ).resolves.toBeInTheDocument();

    // eslint-disable-next-line fp/no-mutating-methods
    Object.defineProperty(window, "location", {
      value: { replace: jest.fn() },
      writable: true,
    });

    const closeButton = await screen.findByRole("button");
    userEvent.click(closeButton);

    expect(window.location.replace).toHaveBeenCalledWith(
      "/orgs/testorg/groups/testgroup/scope"
    );

    mockedFetch.reset();
  });

  it("should restore incomplete process", async (): Promise<void> => {
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
            organizations: [
              {
                country: "Colombia",
                groups: [{ name: "testGroup" }],
                name: "testOrg",
              },
            ],
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
    const rootMock: MockedResponse<IAddGitRootResult> = {
      request: {
        query: ADD_GIT_ROOT,
        variables: {
          branch: "main",
          credentials: {
            key: variables.credentials.key,
            name: variables.credentials.name,
            password: variables.credentials.password,
            token: variables.credentials.token,
            type: variables.credentials.type,
            user: variables.credentials.user,
          },
          environment: "production",
          gitignore: [],
          groupName: "TESTGROUP",
          includesHealthCheck: false,
          nickname: "",
          url: variables.url,
          useVpn: false,
        },
      },
      result: {
        data: {
          addGitRoot: { success: true },
        },
      },
    };

    const mockedFetch = fetch as FetchMockStatic & typeof fetch;
    mockedFetch.mock(EMAIL_DOMAINS_URL, { status: 200, text: "" });
    mockedFetch.mock(COUNTRIES_URL, {
      body: [{ id: 48, name: "Colombia" }],
      status: 200,
    });

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[groupsMock, accessMock, rootMock]}
        >
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

    const nextButton = await screen.findByText("autoenrollment.next");
    userEvent.click(nextButton);

    const orgNameInput = await screen.findByRole("textbox", {
      name: "organizationName",
    });
    const groupNameInput = await screen.findByRole("textbox", {
      name: "groupName",
    });
    const countrySelect = await screen.findByRole("combobox", {
      name: "organizationCountry",
    });

    expect(orgNameInput).toHaveDisplayValue("testOrg");
    expect(groupNameInput).toHaveDisplayValue("testGroup");
    expect(countrySelect).toHaveDisplayValue("Colombia");

    const languageSelect = await screen.findByRole("combobox", {
      name: "reportLanguage",
    });
    userEvent.selectOptions(languageSelect, ["EN"]);

    const groupDescriptionInput = await screen.findByRole("textbox", {
      name: "groupDescription",
    });
    userEvent.type(groupDescriptionInput, "test description");

    const startTrialButton = await screen.findByText("autoenrollment.proceed");
    userEvent.click(startTrialButton);

    await expect(
      screen.findByText("autoenrollment.standby.title")
    ).resolves.toBeInTheDocument();

    // eslint-disable-next-line fp/no-mutating-methods
    Object.defineProperty(window, "location", {
      value: { replace: jest.fn() },
      writable: true,
    });

    const closeButton = await screen.findByRole("button");
    userEvent.click(closeButton);

    expect(window.location.replace).toHaveBeenCalledWith(
      "/orgs/testorg/groups/testgroup/scope"
    );

    mockedFetch.reset();
  });
});
