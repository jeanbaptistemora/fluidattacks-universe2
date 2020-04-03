import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";

import * as React from "react";
import { ActionButtons, IActionButtonsProps } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("ActionButtons", () => {

  const mockProps: IActionButtonsProps = {
    isEditing: false,
    isPristine: false,
    isRemediated: false,
    isRequestingVerify: false,
    isVerified: false,
    isVerifying: false,
    lastTreatment: {
      acceptanceDate: "",
      acceptanceStatus: "",
      date: "",
      justification: "",
      treatment: "",
      user: "",
    },
    onApproveAcceptation: (): void => undefined,
    onEdit: (): void => undefined,
    onRejectAcceptation: (): void => undefined,
    onRequestVerify: (): void => undefined,
    onUpdate: (): void => undefined,
    onVerify: (): void => undefined,
    state: "open",
    subscription: "",
    userRole: "",
  };

  it("should return a function", () => {
    expect(typeof (ActionButtons))
      .toEqual("function");
  });

  it("should render a component", async () => {
    const wrapper: ShallowWrapper = shallow(
      <ActionButtons {...mockProps} />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
