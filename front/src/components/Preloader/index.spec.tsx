import { Preloader } from "./index";
import React from "react";
import { default as loadingAnim } from "../../resources/loading.gif";
import { default as style } from "./index.css";
import { ShallowWrapper, shallow } from "enzyme";

describe("Preloader", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Preloader).toStrictEqual("function");
  });

  it("should render a preloader", (): void => {
    expect.hasAssertions();
    const wrapper: ShallowWrapper = shallow(<Preloader />);
    const element: JSX.Element = (
      <div className={style.loader} id={"full_loader"}>
        <img height={"100"} src={loadingAnim} width={"100"} />
      </div>
    );
    expect(wrapper.contains(element)).toBe(true);
  });
});
