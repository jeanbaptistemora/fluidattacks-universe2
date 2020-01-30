import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { TreatmentView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("FindingTreatment", (): void => {

  it("should return a function", (): void => {
    expect(typeof (TreatmentView))
      .toEqual("function");
  });

  it("should render", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <TreatmentView findingId="413372600" isEditing={false} />,
    );
    expect(wrapper)
      .toHaveLength(1);
  });
});
