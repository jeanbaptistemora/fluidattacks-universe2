import { combineReducers, Reducer } from "redux";
import { reducer as formReducer } from "redux-form";
import { dashboard } from "../scenes/Dashboard/reducer";

const rootReducer: Reducer = combineReducers({
  dashboard,
  form: formReducer,
});

export = rootReducer;
