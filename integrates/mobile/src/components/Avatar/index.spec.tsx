import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { Avatar as PaperAvatar } from "react-native-paper";

import { Avatar } from "./index";

describe("Avatar", (): void => {

  it("should return a function", (): void => {
    expect(typeof (Avatar))
      .toEqual("function");
  });

  it("should render initials", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <Avatar
        photoUrl={undefined}
        userName="Simón José Antonio de la Santísima Trinidad Bolívar y Palacios Ponte-Andrade y Blanco"
        size={40}
      />,
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper
      .render()
      .text())
      .toEqual("SJ");
  });

  it("should render profile picture", (): void => {
    const wrapper: ShallowWrapper = shallow(
      <Avatar
        photoUrl="https://some.com/image.png"
        userName="Test"
        size={40}
      />,
    );

    expect(wrapper)
      .toHaveLength(1);
    expect(wrapper
      .find(PaperAvatar.Image))
      .toHaveLength(1);
  });
});
