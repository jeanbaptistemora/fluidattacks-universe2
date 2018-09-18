import { combineReducers, Reducer } from "redux";
import dashboard from "../scenes/Dashboard/reducer";
import registration from "../scenes/Registration/reducer";

const rootReducer: Reducer = combineReducers({
  dashboard,
  registration,
});

export = rootReducer;
