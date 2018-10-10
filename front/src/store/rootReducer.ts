import { combineReducers, Reducer } from "redux";
import { reducer as formReducer } from "redux-form";
import dashboard from "../scenes/Dashboard/reducer";
import registration from "../scenes/Registration/reducer";

const rootReducer: Reducer = combineReducers({
  dashboard,
  form: formReducer,
  registration,
});

export = rootReducer;
