import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import React from "react";
import { Preloader } from "./index";
import { default as style } from "./index.css";

configure({ adapter: new ReactSixteenAdapter() });

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
          src="assets/img/loading.gif"
          width="100"
          height="100"
        />
      </div>);
    expect(wrapper.contains(element))
      .toBeTruthy();
  });

});
