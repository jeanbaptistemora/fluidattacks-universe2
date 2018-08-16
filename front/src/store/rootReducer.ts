import { combineReducers, Reducer } from "redux";
import registration from "./Registration/reducer";

const rootReducer: Reducer = combineReducers({
  registration,
});

export = rootReducer;
