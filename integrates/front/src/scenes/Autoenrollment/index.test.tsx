import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
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
            trial: null,
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

  it("should render already in trial", async (): Promise<void> => {
    expect.hasAssertions();

    const groupsMock: MockedResponse<IGetStakeholderGroupsResult> = {
      request: {
        query: GET_STAKEHOLDER_GROUPS,
      },
      result: {
        data: {
          me: {
            organizations: [],
            trial: {
              completed: false,
              startDate: "2022-12-06T07:40:16.114232",
            },
            userEmail: "jdoe@fluidattacks.com",
          },
        },
      },
    };

    const mockedFetch = fetch as FetchMockStatic & typeof fetch;
    mockedFetch.mock(EMAIL_DOMAINS_URL, { status: 200, text: "" });
    mockedFetch.mock(COUNTRIES_URL, { body: "[]", status: 200 });

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider cache={getCache()} mocks={[groupsMock]}>
          <Autoenrollment />
        </MockedProvider>
      </MemoryRouter>
    );

    await expect(
      screen.findByText("autoenrollment.alreadyInTrial")
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
            trial: null,
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
    await userEvent.type(urlInput, variables.url);

    const branchInput = await screen.findByRole("textbox", { name: "branch" });
    await userEvent.type(branchInput, variables.branch);

    const credentialsTypeSelect = await screen.findByRole("combobox", {
      name: "credentials.typeCredential",
    });
    await userEvent.selectOptions(credentialsTypeSelect, ["TOKEN"]);

    const credentialsNameInput = await screen.findByRole("textbox", {
      name: "credentials.name",
    });
    await userEvent.type(credentialsNameInput, variables.credentials.name);

    const credentialsTokenInput = await screen.findByRole("textbox", {
      name: "credentials.token",
    });
    await userEvent.type(credentialsTokenInput, variables.credentials.token);

    const credentialsOrganizationInput = await screen.findByRole("textbox", {
      name: "credentials.azureOrganization",
    });
    await userEvent.type(credentialsOrganizationInput, "testorg1");

    const environmentInput = await screen.findByRole("textbox", {
      name: "env",
    });
    await userEvent.type(environmentInput, "production");

    const submitButton = await screen.findByText("autoenrollment.next");
    await userEvent.click(submitButton);

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
            trial: null,
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
    await userEvent.type(urlInput, variables.url);

    const branchInput = await screen.findByRole("textbox", { name: "branch" });
    await userEvent.type(branchInput, variables.branch);

    expect(
      screen.getByRole("combobox", { name: "credentials.typeCredential" })
    ).toHaveValue("");

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "credentials.typeCredential" }),
      ["SSH"]
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "credentials.key" })
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByRole("textbox", { name: "credentials.password" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.user" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.azureOrganization" })
    ).not.toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "credentials.typeCredential" }),
      ["TOKEN"]
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "credentials.azureOrganization" })
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByRole("textbox", { name: "credentials.key" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.password" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.user" })
    ).not.toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "credentials.typeCredential" }),
      ["USER"]
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "credentials.user" })
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByRole("textbox", { name: "credentials.key" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.azureOrganization" })
    ).not.toBeInTheDocument();

    const credentialsTypeSelect = await screen.findByRole("combobox", {
      name: "credentials.typeCredential",
    });
    await userEvent.selectOptions(credentialsTypeSelect, ["USER"]);

    const credentialsNameInput = await screen.findByRole("textbox", {
      name: "credentials.name",
    });
    await userEvent.type(credentialsNameInput, variables.credentials.name);

    const credentialsUserInput = await screen.findByRole("textbox", {
      name: "credentials.user",
    });
    await userEvent.type(credentialsUserInput, variables.credentials.user);

    const credentialsPasswordInput = await screen.findByLabelText(
      "autoenrollment.credentials.password"
    );
    await userEvent.type(
      credentialsPasswordInput,
      variables.credentials.password
    );

    const environmentInput = await screen.findByRole("textbox", {
      name: "env",
    });
    await userEvent.type(environmentInput, "production");

    const submitButton = await screen.findByText("autoenrollment.next");
    await userEvent.click(submitButton);

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
            trial: null,
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
    await userEvent.type(urlInput, variables.url);

    const branchInput = await screen.findByRole("textbox", { name: "branch" });
    await userEvent.type(branchInput, variables.branch);

    const credentialsTypeSelect = await screen.findByRole("combobox", {
      name: "credentials.typeCredential",
    });
    await userEvent.selectOptions(credentialsTypeSelect, [
      variables.credentials.type,
    ]);

    const credentialsNameInput = await screen.findByRole("textbox", {
      name: "credentials.name",
    });
    await userEvent.type(credentialsNameInput, variables.credentials.name);

    const credentialsKeyInput = await screen.findByRole("textbox", {
      name: "credentials.key",
    });
    await userEvent.type(
      credentialsKeyInput,
      "-----BEGIN OPENSSH PRIVATE KEY-----\ntest\n-----END OPENSSH PRIVATE KEY-----"
    );

    const environmentInput = await screen.findByRole("textbox", {
      name: "env",
    });
    await userEvent.type(environmentInput, "production");

    const submitButton = await screen.findByText("autoenrollment.next");
    await userEvent.click(submitButton);

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
            trial: null,
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
            azureOrganization: undefined,
            isPat: false,
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
    await userEvent.type(urlInput, variables.url);

    const branchInput = await screen.findByRole("textbox", { name: "branch" });
    await userEvent.type(branchInput, variables.branch);

    const credentialsTypeSelect = await screen.findByRole("combobox", {
      name: "credentials.typeCredential",
    });
    await userEvent.selectOptions(credentialsTypeSelect, [
      variables.credentials.type,
    ]);

    const credentialsNameInput = await screen.findByRole("textbox", {
      name: "credentials.name",
    });
    await userEvent.type(credentialsNameInput, variables.credentials.name);

    const credentialsKeyInput = await screen.findByRole("textbox", {
      name: "credentials.key",
    });
    await userEvent.type(
      credentialsKeyInput,
      "-----BEGIN OPENSSH PRIVATE KEY-----\ntest\n-----END OPENSSH PRIVATE KEY-----"
    );

    const environmentInput = await screen.findByRole("textbox", {
      name: "env",
    });
    await userEvent.type(environmentInput, "production");

    const nextButton = await screen.findByText("autoenrollment.next");
    await userEvent.click(nextButton);

    const orgNameInput = await screen.findByRole("textbox", {
      name: "organizationName",
    });
    await userEvent.type(orgNameInput, "testOrg");

    const groupNameInput = await screen.findByRole("textbox", {
      name: "groupName",
    });
    await userEvent.type(groupNameInput, "testGroup");

    const countrySelect = await screen.findByRole("combobox", {
      name: "organizationCountry",
    });
    await userEvent.selectOptions(countrySelect, ["Colombia"]);

    const languageSelect = await screen.findByRole("combobox", {
      name: "reportLanguage",
    });
    await userEvent.selectOptions(languageSelect, ["EN"]);

    const groupDescriptionInput = await screen.findByRole("textbox", {
      name: "groupDescription",
    });
    await userEvent.type(groupDescriptionInput, "test description");

    const startTrialButton = await screen.findByText("autoenrollment.proceed");
    await userEvent.click(startTrialButton);

    // eslint-disable-next-line fp/no-mutating-methods
    Object.defineProperty(window, "location", {
      value: { replace: jest.fn() },
      writable: true,
    });

    const closeButton = await screen.findByRole("button");
    await userEvent.click(closeButton);

    expect(window.location.replace).toHaveBeenCalledWith(
      "/orgs/testorg/groups/testgroup/vulns"
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
            trial: null,
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
            azureOrganization: undefined,
            isPat: false,
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
    await userEvent.type(urlInput, variables.url);

    const branchInput = await screen.findByRole("textbox", { name: "branch" });
    await userEvent.type(branchInput, variables.branch);

    const credentialsTypeSelect = await screen.findByRole("combobox", {
      name: "credentials.typeCredential",
    });
    await userEvent.selectOptions(credentialsTypeSelect, [
      variables.credentials.type,
    ]);

    const credentialsNameInput = await screen.findByRole("textbox", {
      name: "credentials.name",
    });
    await userEvent.type(credentialsNameInput, variables.credentials.name);

    const credentialsKeyInput = await screen.findByRole("textbox", {
      name: "credentials.key",
    });
    await userEvent.type(
      credentialsKeyInput,
      "-----BEGIN OPENSSH PRIVATE KEY-----\ntest\n-----END OPENSSH PRIVATE KEY-----"
    );

    const environmentInput = await screen.findByRole("textbox", {
      name: "env",
    });
    await userEvent.type(environmentInput, "production");

    const nextButton = await screen.findByText("autoenrollment.next");
    await userEvent.click(nextButton);

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
    expect(orgNameInput).toBeDisabled();
    expect(groupNameInput).toHaveDisplayValue("testGroup");
    expect(groupNameInput).toBeDisabled();
    expect(countrySelect).toHaveDisplayValue("Colombia");
    expect(countrySelect).toBeDisabled();

    const languageSelect = await screen.findByRole("combobox", {
      name: "reportLanguage",
    });
    await userEvent.selectOptions(languageSelect, ["EN"]);

    const groupDescriptionInput = await screen.findByRole("textbox", {
      name: "groupDescription",
    });
    await userEvent.type(groupDescriptionInput, "test description");

    const startTrialButton = await screen.findByText("autoenrollment.proceed");
    await userEvent.click(startTrialButton);

    // eslint-disable-next-line fp/no-mutating-methods
    Object.defineProperty(window, "location", {
      value: { replace: jest.fn() },
      writable: true,
    });

    const closeButton = await screen.findByRole("button");
    await userEvent.click(closeButton);

    expect(window.location.replace).toHaveBeenCalledWith(
      "/orgs/testorg/groups/testgroup/vulns"
    );

    mockedFetch.reset();
  });
});
