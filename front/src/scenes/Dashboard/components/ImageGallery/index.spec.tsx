import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import ReactImageGallery from "react-image-gallery";
import { default as ImageGallery } from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Image Gallery", () => {

  it("should return a function", () => {
    expect(typeof (ImageGallery))
      .toEqual("function");
  });

  it("should render image gallery", () => {
    const data: object[] = [
      {
        original: "image.png",
        originalTitle: "This is a title",
      },
    ];

    const wrapper: ShallowWrapper = shallow(
      <ImageGallery
        items={data}
      />,
    );

    expect(wrapper.find(ReactImageGallery))
      .toHaveLength(1);
  });
});
