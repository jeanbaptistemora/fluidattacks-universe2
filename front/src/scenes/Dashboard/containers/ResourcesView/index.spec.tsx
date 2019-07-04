import { configure } from "enzyme";
import ReactSixteenAdapter from "enzyme-adapter-react-16";
// tslint:disable-next-line: no-import-side-effect
import "isomorphic-fetch";
import ProjectResourcesView from "./index";

configure({ adapter: new ReactSixteenAdapter() });

describe("Resources view", () => {
  it("should return a object", () => {
    expect(typeof (ProjectResourcesView))
      .toEqual("object");
  });
});
