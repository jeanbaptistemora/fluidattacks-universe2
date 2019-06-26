import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { component as EvidenceView } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Evidence view", () => {

  it("should return a function", () => {
    expect(typeof (EvidenceView))
      .toEqual("function");
  });

  it("should render lightbox", () => {
    const wrapper: ShallowWrapper = shallow(
      <EvidenceView
        canEdit={true}
        currentIndex={0}
        findingId="438679960"
        images={[{ description: "Test evidence", url: "https://test.com/test.png" }]}
        isEditing={false}
        isImageOpen={true}
      />,
    );

    expect(wrapper.find("ReactImageLightbox").length)
      .toEqual(1);
  });
});
