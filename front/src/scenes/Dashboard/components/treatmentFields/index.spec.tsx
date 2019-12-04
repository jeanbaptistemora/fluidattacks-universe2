import { configure } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
import TreatmentFieldsView from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Treatment Fields", () => {

  it("should return a function", () => {
    expect(typeof (TreatmentFieldsView))
      .toEqual("function");
  });
});
