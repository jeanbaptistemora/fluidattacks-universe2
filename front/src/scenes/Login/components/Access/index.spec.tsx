import { expect } from "chai";
import { configure } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import { describe, it } from "mocha";
import Access from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Login", () => {

  it("should return a function", () => {
    expect(typeof (Access)).to
      .equal("function");
  });

});
