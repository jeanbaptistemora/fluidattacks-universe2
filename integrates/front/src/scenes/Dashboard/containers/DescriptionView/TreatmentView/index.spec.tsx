import { MockedProvider, MockedResponse, wait } from "@apollo/react-testing";
import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
// tslint:disable-next-line: no-submodule-imports
import { act } from "react-dom/test-utils";
import { Provider } from "react-redux";
import { ITreatmentViewProps, TreatmentView } from "scenes/Dashboard/containers/DescriptionView/TreatmentView";
import { GET_FINDING_TREATMENT } from "scenes/Dashboard/containers/DescriptionView/TreatmentView/queries";
import store from "store";

describe("Finding Treatment", () => {

  const baseMockProps: ITreatmentViewProps = {
    approvalModalConfig: { open: false, type: "" },
    findingId: "413372600",
    isEditing: false,
    onCloseApproval: jest.fn(),
    projectName: "TEST",
    setEditing: jest.fn(),
  };

  const treatmentQuery: Readonly<MockedResponse> = {
    request: {
      query: GET_FINDING_TREATMENT,
      variables: {
        canRetrieveAnalyst: true,
        findingId: "413372600",
        projectName: "TEST",
      },
    },
    result: {
      data: {
        finding: {
          btsUrl: "https://gitlab.com/fluidattacks/something/-/issues",
          historicTreatment: [],
          id: "413372600",
          openVulnerabilities: 0,
        },
      },
    },
  };

  it("should return a function", () => {
    expect(typeof (TreatmentView))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <Provider store={store}>
        <MockedProvider mocks={[treatmentQuery]} addTypename={false}>
          <TreatmentView {...baseMockProps} />
        </MockedProvider>
      </Provider>,
    );
    await act(async () => { await wait(50); wrapper.update(); });
    expect(wrapper)
      .toHaveLength(1);
  });
});
