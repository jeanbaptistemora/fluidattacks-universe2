import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { component as RecordsView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Records view", () => {

  it("should return a function", () => {
    expect(typeof (RecordsView)).to
      .equal("function");
  });

  it("should render", () => {
    const wrapper: ShallowWrapper = shallow(
      <RecordsView
        canEdit={true}
        findingId="422286126"
        dataset={[]}
        isEditing={true}
      />,
    );

    expect(wrapper).to.have
      .length(1);
  });
});
