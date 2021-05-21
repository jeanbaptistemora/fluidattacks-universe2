import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import type { ReactWrapper } from "enzyme";
import { mount } from "enzyme";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route } from "react-router-dom";
import waitForExpect from "wait-for-expect";

import { FindingPolicies } from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/index";
import {
  ADD_ORGANIZATION_FINDING_POLICY,
  GET_ORGANIZATION_FINDINGS_TITLES,
} from "scenes/Dashboard/containers/OrganizationPoliciesView/FindingPolicies/queries";
import { GET_ORGANIZATION_POLICIES } from "scenes/Dashboard/containers/OrganizationPoliciesView/queries";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../utils/notifications",
  (): Dictionary => {
    const mockedNotifications: Dictionary<
      () => Dictionary
    > = jest.requireActual("../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("Organization findings policies view", (): void => {
  const organizationId: string = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3";
  const mockFindingTitleQuery: MockedResponse = {
    request: {
      query: GET_ORGANIZATION_FINDINGS_TITLES,
      variables: {
        organizationId,
      },
    },
    result: {
      data: {
        organization: {
          id: organizationId,
          name: "okada",
          projects: [
            {
              findings: [
                {
                  id: "422286126",
                  title: "F060. Insecure exceptions",
                },
                {
                  id: "836530833",
                  title: "F004. Ejecución remota de comandos",
                },
              ],
              name: "unitestting",
            },
          ],
        },
      },
    },
  };

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
              name: "F060. Insecure exceptions",
              status: "SUBMITTED",
            },
          ],
          maxAcceptanceDays: null,
          maxAcceptanceSeverity: 10,
          maxNumberAcceptations: null,
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

    const mockMutation: MockedResponse = {
      request: {
        query: ADD_ORGANIZATION_FINDING_POLICY,
        variables: {
          name: "F060. Insecure exceptions",
          organizationName: "okada",
        },
      },
      result: {
        data: {
          addOrgFindingPolicy: {
            success: true,
          },
        },
      },
    };

    const wrapper: ReactWrapper = mount(
      <MemoryRouter initialEntries={["/orgs/okada/policies"]}>
        <MockedProvider
          addTypename={false}
          mocks={[mockFindingTitleQuery, mockQuery, mockMutation]}
        >
          <Route path={"/orgs/:organizationName/policies"}>
            <FindingPolicies
              findingPolicies={[]}
              organizationId={organizationId}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(
      async (): Promise<void> => {
        expect.hasAssertions();

        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper).toHaveLength(1);
        });
      }
    );

    const name: ReactWrapper = wrapper.find({ name: "name" }).find("input");

    name.simulate("change", {
      target: { name: "name", value: "F060. Insecure exceptions" },
    });

    wrapper.find("Formik").simulate("submit");

    await act(
      async (): Promise<void> => {
        expect.hasAssertions();

        wrapper.update();

        await waitForExpect((): void => {
          expect(msgSuccess).toHaveBeenCalledTimes(1);
        });
      }
    );
  });

  it("add organization findings policies mutation message error", async (): Promise<void> => {
    expect.hasAssertions();

    const mockMutation: MockedResponse = {
      request: {
        query: ADD_ORGANIZATION_FINDING_POLICY,
        variables: {
          name: "F060. Insecure exceptions",
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
        <MockedProvider
          addTypename={false}
          mocks={[mockFindingTitleQuery, mockQuery, mockMutation]}
        >
          <Route path={"/orgs/:organizationName/policies"}>
            <FindingPolicies
              findingPolicies={[
                {
                  id: "97ad7167-51aa-4214-a612-16a833df6565",
                  lastStatusUpdate: "2021-05-21T06:16:48",
                  name: "F060. Insecure exceptions",
                  status: "APPROVED",
                },
              ]}
              organizationId={organizationId}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await act(
      async (): Promise<void> => {
        expect.hasAssertions();

        await waitForExpect((): void => {
          wrapper.update();

          expect(wrapper).toHaveLength(1);
        });
      }
    );

    const name: ReactWrapper = wrapper.find({ name: "name" }).find("input");

    name.simulate("change", {
      target: { name: "name", value: "F060. Insecure exceptions" },
    });

    wrapper.find("Formik").simulate("submit");

    await act(
      async (): Promise<void> => {
        expect.hasAssertions();

        wrapper.update();

        await waitForExpect((): void => {
          expect(msgError).toHaveBeenCalledWith(
            t("organization.tabs.policies.findings.errors.duplicateFinding")
          );
        });
      }
    );
  });
});
