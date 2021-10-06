/* eslint-disable camelcase */
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import type { FetchMockStatic } from "fetch-mock";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route } from "react-router-dom";
import wait from "waait";
import waitForExpect from "wait-for-expect";

import { FindingPolicies } from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/index";
import {
  ADD_ORGANIZATION_FINDING_POLICY,
  DEACTIVATE_ORGANIZATION_FINDING_POLICY,
  HANDLE_ORGANIZATION_FINDING_POLICY,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/queries";
import { GET_ORGANIZATION_POLICIES } from "scenes/Dashboard/containers/OrganizationPoliciesView/queries";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const mockedFetch: FetchMockStatic = fetch as FetchMockStatic & typeof fetch;
const baseUrl: string =
  "https://gitlab.com/api/v4/projects/20741933/repository/files";
const branchRef: string = "master";
const vulnsFileId: string =
  "makes%2Ffoss%2Fmodules%2Fmakes%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml";
mockedFetch.mock(`${baseUrl}/${vulnsFileId}/raw?ref=${branchRef}`, {
  body: {
    "060": {
      en: {
        description: "",
        impact: "",
        recommendation: "",
        threat: "",
        title: "Insecure exceptions",
      },
      requirements: [],
      score: {
        base: {
          attack_complexity: "",
          attack_vector: "",
          availability: "",
          confidentiality: "",
          integrity: "",
          privileges_required: "",
          scope: "",
          user_interaction: "",
        },
        temporal: {
          exploit_code_maturity: "",
          remediation_level: "",
          report_confidence: "",
        },
      },
    },
  },

  status: 200,
});
const requirementsFileId: string =
  "makes%2Ffoss%2Fmodules%2Fmakes%2Fcriteria%2Fsrc%2Frequirements%2Fdata.yaml";
mockedFetch.mock(`${baseUrl}/${requirementsFileId}/raw?ref=${branchRef}`, {
  body: {
    "161": {
      category: "",
      en: {
        description: "",
        summary: `
          The source code
          must have secure default options
          ensuring secure failures
          in the application
          (try, catch/except; default for switches).
        `,
        title: "Define secure default options",
      },
      references: [],
    },
    "359": {
      category: "",
      en: {
        description: "",
        summary: `
          The system should use
          typified exceptions instead of
          generic exceptions.
        `,
        title: "Avoid using generic exceptions",
      },
      references: [],
    },
  },

  status: 200,
});

jest.mock("../../../../../utils/notifications", (): Dictionary => {
  const mockedNotifications: Dictionary<() => Dictionary> = jest.requireActual(
    "../../../../../utils/notifications"
  );
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Organization findings policies view", (): void => {
  const organizationId: string = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3";

  const mockQuery: MockedResponse = {
    request: {
      query: GET_ORGANIZATION_POLICIES,
      variables: {
        organizationId,
      },
    },
    result: {
      data: {
        organization: {
          findingPolicies: [
            {
              id: "97ad7167-51aa-4214-a612-16a833df6565",
              lastStatusUpdate: "2021-05-20T15:16:48",
              name: "060. Insecure exceptions",
              status: "SUBMITTED",
            },
          ],
          maxAcceptanceDays: null,
          maxAcceptanceSeverity: 10,
          maxNumberAcceptances: null,
          minAcceptanceSeverity: 0,
          name: "okada",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof FindingPolicies).toStrictEqual("function");
  });

  it("add organization findings policies mutation", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockMutation: MockedResponse = {
      request: {
        query: ADD_ORGANIZATION_FINDING_POLICY,
        variables: {
          name: "060. Insecure exceptions",
          organizationName: "okada",
        },
      },
      result: {
        data: {
          addOrganizationFindingPolicy: {
            success: true,
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={[mockQuery, mockMutation]}>
          <Route path={"/orgs/:organizationName/policies"}>
            <FindingPolicies
              findingPolicies={[]}
              organizationId={organizationId}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
      });
    });

    const name: ReactWrapper = wrapper.find({ name: "name" }).find("input");

    name.simulate("change", {
      target: { name: "name", value: "060. Insecure exceptions" },
    });

    wrapper.find("Formik").simulate("submit");

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      wrapper.update();

      await waitForExpect((): void => {
        expect(msgSuccess).toHaveBeenCalledTimes(1);
      });
    });
  });

  it("add organization findings policies mutation message error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockMutation: MockedResponse = {
      request: {
        query: ADD_ORGANIZATION_FINDING_POLICY,
        variables: {
          name: "060. Insecure exceptions",
          organizationName: "okada",
        },
      },
      result: {
        errors: [
          new GraphQLError(
            "Exception - The finding name policy already exists"
          ),
        ],
      },
    };

    const { t } = useTranslation();
    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={[mockQuery, mockMutation]}>
          <Route path={"/orgs/:organizationName/policies"}>
            <FindingPolicies
              findingPolicies={[
                {
                  id: "97ad7167-51aa-4214-a612-16a833df6565",
                  lastStatusUpdate: "2021-05-21T06:16:48",
                  name: "060. Insecure exceptions",
                  status: "APPROVED",
                  tags: [],
                },
              ]}
              organizationId={organizationId}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
      });
    });

    const name: ReactWrapper = wrapper.find({ name: "name" }).find("input");

    name.simulate("change", {
      target: { name: "name", value: "060. Insecure exceptions" },
    });

    wrapper.find("Formik").simulate("submit");

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      wrapper.update();

      await waitForExpect((): void => {
        expect(msgError).toHaveBeenCalledWith(
          t("organization.tabs.policies.findings.errors.duplicateFinding")
        );
      });
    });
  });

  it("organization finding policy missing handle actions permissions", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={[mockQuery]}>
          <Route path={"/orgs/:organizationName/policies"}>
            <FindingPolicies
              findingPolicies={[
                {
                  id: "fd882d65-1c25-41c5-9bd1-e3ef5200e7cd",
                  lastStatusUpdate: "2021-05-21T06:58:58",
                  name: "060. Insecure exceptions",
                  status: "SUBMITTED",
                  tags: [],
                },
                {
                  id: "0b61d5bc-abcc-47e1-9293-f2ff76f4fc17",
                  lastStatusUpdate: "2021-05-21T05:58:58",
                  name: "004. Remote command execution",
                  status: "APPROVED",
                  tags: [],
                },
              ]}
              organizationId={organizationId}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    const firstRow: ReactWrapper = wrapper
      .find("OrganizationFindingPolicy")
      .first();
    const lastRow: ReactWrapper = wrapper
      .find("OrganizationFindingPolicy")
      .last();

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      wrapper.update();

      await waitForExpect((): void => {
        expect(firstRow.find("Button")).toHaveLength(0);
        expect(lastRow.find("Button")).toHaveLength(0);
      });
    });
  });

  it("organization finding policy handle actions permissions", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockHandleMutation: MockedResponse[] = [
      {
        request: {
          query: HANDLE_ORGANIZATION_FINDING_POLICY,
          variables: {
            findingPolicyId: "923f081c-eae2-4ab7-9c66-36b12fd554d7",
            organizationName: "okada",
            status: "APPROVED",
          },
        },
        result: {
          data: {
            handleOrganizationFindingPolicyAcceptance: {
              success: true,
            },
          },
        },
      },
      mockQuery,
    ];

    const mockDeactivateMutation: MockedResponse[] = [
      {
        request: {
          query: DEACTIVATE_ORGANIZATION_FINDING_POLICY,
          variables: {
            findingPolicyId: "7960b957-0d57-40fb-8053-24f064d68000",
            organizationName: "okada",
          },
        },
        result: {
          data: {
            deactivateOrganizationFindingPolicy: {
              success: true,
            },
          },
        },
      },
      mockQuery,
    ];

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider
          addTypename={false}
          mocks={[...mockDeactivateMutation, ...mockHandleMutation]}
        >
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                {
                  action:
                    "api_mutations_handle_organization_finding_policy_acceptation_mutate",
                },
                {
                  action:
                    "api_mutations_deactivate_organization_finding_policy_mutate",
                },
              ])
            }
          >
            <Route path={"/orgs/:organizationName/policies"}>
              <FindingPolicies
                findingPolicies={[
                  {
                    id: "923f081c-eae2-4ab7-9c66-36b12fd554d7",
                    lastStatusUpdate: "2021-05-21T07:16:48",
                    name: "060. Insecure exceptions",
                    status: "SUBMITTED",
                    tags: [],
                  },
                  {
                    id: "7960b957-0d57-40fb-8053-24f064d68000",
                    lastStatusUpdate: "2021-05-21T08:58:58",
                    name: "004. Remote command execution",
                    status: "APPROVED",
                    tags: [],
                  },
                ]}
                organizationId={organizationId}
              />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    const firstRow: ReactWrapper = wrapper
      .find("OrganizationFindingPolicy")
      .first();

    const lastRow: ReactWrapper = wrapper
      .find("OrganizationFindingPolicy")
      .last();

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      wrapper.update();

      await waitForExpect((): void => {
        expect(firstRow.find("Button")).toHaveLength(2);
        expect(lastRow.find("Button")).toHaveLength(1);
      });
    });

    firstRow.find("Button").first().simulate("click");
    await act(async (): Promise<void> => {
      expect.hasAssertions();

      wrapper.update();

      await waitForExpect((): void => {
        expect(msgSuccess).toHaveBeenCalledWith(
          translate.t(
            "organization.tabs.policies.findings.handlePolicies.success.approved"
          ),
          translate.t("sidebar.newOrganization.modal.successTitle")
        );
      });
    });

    lastRow.find("Button").first().simulate("click");
    await act(async (): Promise<void> => {
      expect.hasAssertions();

      wrapper.update();

      await waitForExpect((): void => {
        expect(wrapper.find("ConfirmDialog")).toHaveLength(1);
      });
    });

    const confirmDialog: ReactWrapper = wrapper.find("ConfirmDialog").first();

    const proceedButton: ReactWrapper = confirmDialog
      .find("button")
      .findWhere((element: ReactWrapper): boolean =>
        element.contains("Proceed")
      )
      .first();
    proceedButton.simulate("click");
    await act(async (): Promise<void> => {
      expect.hasAssertions();

      wrapper.update();

      await waitForExpect((): void => {
        expect(msgSuccess).toHaveBeenCalledWith(
          translate.t(
            "organization.tabs.policies.findings.deactivatePolicies.success"
          ),
          translate.t("sidebar.newOrganization.modal.successTitle")
        );
      });
    });
  });

  it("organization finding policy handle reject action", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockHandleMutation: MockedResponse[] = [
      {
        request: {
          query: HANDLE_ORGANIZATION_FINDING_POLICY,
          variables: {
            findingPolicyId: "08207180-305f-4f97-b727-ea29d5199590",
            organizationName: "okada",
            status: "REJECTED",
          },
        },
        result: {
          data: {
            handleOrganizationFindingPolicyAcceptance: {
              success: true,
            },
          },
        },
      },
      mockQuery,
    ];

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={mockHandleMutation}>
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                {
                  action:
                    "api_mutations_handle_organization_finding_policy_acceptation_mutate",
                },
                {
                  action:
                    "api_mutations_deactivate_organization_finding_policy_mutate",
                },
              ])
            }
          >
            <Route path={"/orgs/:organizationName/policies"}>
              <FindingPolicies
                findingPolicies={[
                  {
                    id: "08207180-305f-4f97-b727-ea29d5199590",
                    lastStatusUpdate: "2021-05-21T11:16:48",
                    name: "060. Insecure exceptions",
                    status: "SUBMITTED",
                    tags: [],
                  },
                  {
                    id: "0e14b989-407d-4c53-a506-25e784378569",
                    lastStatusUpdate: "2021-05-21T11:58:58",
                    name: "004. Remote command execution",
                    status: "APPROVED",
                    tags: [],
                  },
                ]}
                organizationId={organizationId}
              />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    const firstRow: ReactWrapper = wrapper
      .find("OrganizationFindingPolicy")
      .first();

    const lastRow: ReactWrapper = wrapper
      .find("OrganizationFindingPolicy")
      .last();

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      wrapper.update();

      await waitForExpect((): void => {
        expect(firstRow.find("Button")).toHaveLength(2);
        expect(lastRow.find("Button")).toHaveLength(1);
      });
    });

    firstRow.find("Button").last().simulate("click");
    await act(async (): Promise<void> => {
      expect.hasAssertions();

      wrapper.update();

      await waitForExpect((): void => {
        expect(msgSuccess).toHaveBeenCalledWith(
          translate.t(
            "organization.tabs.policies.findings.handlePolicies.success.rejected"
          ),
          translate.t("sidebar.newOrganization.modal.successTitle")
        );
      });
    });

    lastRow.find("Button").first().simulate("click");
    await act(async (): Promise<void> => {
      expect.hasAssertions();

      wrapper.update();

      await waitForExpect((): void => {
        expect(wrapper.find("Modal").first().prop("open")).toBe(true);
      });
    });

    const confirmDialog: ReactWrapper = wrapper.find("ConfirmDialog").first();

    const cancelButton: ReactWrapper = confirmDialog
      .find("button")
      .findWhere((element: ReactWrapper): boolean => element.contains("Cancel"))
      .first();
    cancelButton.simulate("click");
    await act(async (): Promise<void> => {
      expect.hasAssertions();

      wrapper.update();

      await waitForExpect((): void => {
        expect(wrapper.find("Modal").first().prop("open")).toBe(false);
      });
    });
  });

  it("handle organization findings policies mutation message error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockMutation: MockedResponse[] = [
      {
        request: {
          query: HANDLE_ORGANIZATION_FINDING_POLICY,
          variables: {
            findingPolicyId: "97ad7167-51aa-4214-a612-16a833df6565",
            organizationName: "okada",
            status: "APPROVED",
          },
        },
        result: {
          errors: [
            new GraphQLError("Exception - Finding name policy not found"),
            new GraphQLError(
              "Exception - This policy has already been reviewed"
            ),
          ],
        },
      },
      mockQuery,
    ];

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={mockMutation}>
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                {
                  action:
                    "api_mutations_handle_organization_" +
                    "finding_policy_acceptation_mutate",
                },
              ])
            }
          >
            <Route path={"/orgs/:organizationName/policies"}>
              <FindingPolicies
                findingPolicies={[
                  {
                    id: "97ad7167-51aa-4214-a612-16a833df6565",
                    lastStatusUpdate: "2021-05-21T06:16:48",
                    name: "060. Insecure exceptions",
                    status: "SUBMITTED",
                    tags: [],
                  },
                ]}
                organizationId={organizationId}
              />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
      });
    });

    const firstRow: ReactWrapper = wrapper
      .find("OrganizationFindingPolicy")
      .first();

    firstRow.find("Button").first().simulate("click");

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      wrapper.update();

      await waitForExpect((): void => {
        expect(msgError).toHaveBeenCalledTimes(2);
      });
    });
  });

  it("add organization findings policies mutation with tags", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const { t } = useTranslation();

    const mockMutation: MockedResponse = {
      request: {
        query: ADD_ORGANIZATION_FINDING_POLICY,
        variables: {
          name: "060. Insecure exceptions",
          organizationName: "okada",
          tags: ["password", "sessions"],
        },
      },
      result: {
        data: {
          addOrganizationFindingPolicy: {
            success: true,
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider addTypename={false} mocks={[mockQuery, mockMutation]}>
          <Route path={"/orgs/:organizationName/policies"}>
            <FindingPolicies
              findingPolicies={[]}
              organizationId={organizationId}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      await waitForExpect((): void => {
        wrapper.update();

        expect(wrapper).toHaveLength(1);
      });
    });

    const name: ReactWrapper = wrapper
      .find("Field")
      .at(0)
      .find("input")
      .first();
    const tags: ReactWrapper = wrapper
      .find("Field")
      .at(1)
      .find("input")
      .first();

    const ENTER_ARROW_KEY_CODE = 13;
    const DELAY: number = 10;
    await act(async (): Promise<void> => {
      tags.simulate("change", {
        target: { name: "tags", value: "password" },
      });
      await wait(DELAY);

      tags.simulate("keyDown", { keyCode: ENTER_ARROW_KEY_CODE });
      tags.simulate("change", {
        target: { name: "tags", value: "sessions" },
      });
      await wait(DELAY);

      tags.simulate("keyDown", { keyCode: ENTER_ARROW_KEY_CODE });
      name.simulate("change", {
        target: { name: "name", value: "060. Insecure exceptions" },
      });
      wrapper.update();
      await wait(DELAY);
    });

    wrapper.find("Formik").simulate("submit");

    await act(async (): Promise<void> => {
      expect.hasAssertions();

      wrapper.update();

      await waitForExpect((): void => {
        expect(msgSuccess).toHaveBeenCalledWith(
          t("organization.tabs.policies.findings.addPolicies.success"),
          t("sidebar.newOrganization.modal.successTitle")
        );
      });
    });
  });
});
