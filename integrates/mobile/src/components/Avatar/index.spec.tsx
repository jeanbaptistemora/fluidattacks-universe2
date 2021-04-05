import type { ShallowWrapper } from "enzyme";
import { shallow } from "enzyme";
import React from "react";
import { Avatar as PaperAvatar } from "react-native-paper";

import { Avatar } from ".";

describe("Avatar", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Avatar).toStrictEqual("function");
  });

  it("should render initials", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Avatar
        photoUrl={undefined}
        size={40}
        userName={
          "Simón José Antonio de la Santísima Trinidad Bolívar y Palacios Ponte-Andrade y Blanco"
        }
      />
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.render().text()).toStrictEqual("SJ");
  });

  it("should render profile picture", (): void => {
    expect.hasAssertions();

    const wrapper: ShallowWrapper = shallow(
      <Avatar
        photoUrl={"https://some.com/image.png"}
        size={40}
        userName={"Test"}
      />
    );

    expect(wrapper).toHaveLength(1);
    expect(wrapper.find(PaperAvatar.Image)).toHaveLength(1);
  });
});
