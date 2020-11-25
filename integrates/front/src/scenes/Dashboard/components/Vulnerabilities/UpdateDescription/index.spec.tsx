import { MockedProvider } from "@apollo/react-testing";
import { PureAbility } from "@casl/ability";
import { mount, ReactWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import type { IVulnDataType } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateTreatmentModal } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import {
  getLastTreatment,
  groupLastHistoricTreatment,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";
import store from "store";
import { authzPermissionsContext } from "utils/authz/config";
import waitForExpect from "wait-for-expect";

describe("Update Description component", () => {
  const vulns: IVulnDataType[] = [
    {
      currentState: "",
      externalBts: "",
      historicTreatment: [],
      id: "test",
      severity: "",
      specific: "",
      tag: "one",
      treatmentManager: "",
      where: "",
    },
  ];
  const mockedPermissions: PureAbility<string> = new PureAbility([
    { action: "backend_api_resolvers_vulnerability__do_update_treatment_vuln" },
    { action: "backend_api_mutations_update_vulns_treatment_mutate" },
  ]);

  it("should group last treatment", async () => {
    const treatment: IHistoricTreatment = {
      date: "",
      justification: "test justification",
      treatment: "IN PROGRESS",
      user: "",
    };

    const vulnerabilities: IVulnDataType[] = [
      {
        currentState: "",
        externalBts: "",
        historicTreatment: [treatment],
        id: "test_one",
        severity: "",
        specific: "",
        tag: "one",
        treatmentManager: "",
        where: "",
      },
      {
        currentState: "",
        externalBts: "",
        historicTreatment: [treatment],
        id: "test_two",
        severity: "",
        specific: "",
        tag: "one",
        treatmentManager: "",
        where: "",
      },
    ];

    const lastTreatment: IHistoricTreatment = groupLastHistoricTreatment(vulnerabilities);

    expect(lastTreatment)
      .toEqual(getLastTreatment([treatment]));
  });

  it("list editable fields", async () => {
    const handleOnClose: jest.Mock = jest.fn();
    const wrapper: ReactWrapper = mount(
      <Provider store={store}>
        <MockedProvider mocks={[]} addTypename={false}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <UpdateTreatmentModal
              findingId="1"
              vulnerabilities={vulns}
              vulnerabilitiesChunk={1}
              handleCloseModal={handleOnClose}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </Provider>,
    );

    await act(async () => {
      await waitForExpect(() => {
        wrapper.update();
        expect(wrapper)
          .toHaveLength(1);
        expect(wrapper.find({ renderAsEditable: true }))
          .toHaveLength(2);
      });
    });
  });
});
