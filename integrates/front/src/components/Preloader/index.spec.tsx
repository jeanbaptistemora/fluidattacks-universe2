import { Preloader } from "components/Preloader";
import React from "react";
import loadingAnim from "resources/loading.gif";
import style from "components/Preloader/index.css";
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
        <img
          alt={"Loading animation"}
          height={"100"}
          src={loadingAnim}
          width={"100"}
        />
      </div>
    );

    expect(wrapper.contains(element)).toBe(true);
  });
});
