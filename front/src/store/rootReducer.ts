import { combineReducers, Reducer } from "redux";
import { reducer as formReducer } from "redux-form";

const rootReducer: Reducer = combineReducers({ form: formReducer });

export = rootReducer;
