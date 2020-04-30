import { shallow, ShallowWrapper } from "enzyme";
import React from "react";
import { default as loadingAnim } from "../../resources/loading.gif";
import { Preloader } from "./index";
import { default as style } from "./index.css";

describe("Preloader", () => {

  it("should return a function", () => {
    expect(typeof (Preloader))
      .toEqual("function");
  });

  it("should render a preloader", () => {
    const wrapper: ShallowWrapper = shallow((
      <Preloader />
    ));
    const element: JSX.Element = (
      <div id="full_loader" className={style.loader}>
        <img
          src={loadingAnim}
          width="100"
          height="100"
        />
      </div>);
    expect(wrapper.contains(element))
      .toBeTruthy();
  });

});
