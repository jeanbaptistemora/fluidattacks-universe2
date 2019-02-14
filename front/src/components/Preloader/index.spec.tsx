import { expect } from "chai";
import { configure, shallow, ShallowWrapper } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import React from "react";
import { default as Preloader } from "./index";
import style from "./index.css";

configure({ adapter: new ReactSixteenAdapter() });

describe("Preloader", () => {

  it("should return a function", () => {
    expect(typeof (Preloader)).to
      .equal("function");
  });

  it("should be render", () => {
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
    expect(wrapper.contains(element)).to
      .equal(true);
  });

});
