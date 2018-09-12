import { combineReducers, Reducer } from "redux";
import registration from "../scenes/Registration/reducer";

const rootReducer: Reducer = combineReducers({
  registration,
});

export = rootReducer;
