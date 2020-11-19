import type { Reducer } from "redux";
import { combineReducers } from "redux";
import { reducer as formReducer } from "redux-form";

const rootReducer: Reducer = combineReducers({ form: formReducer });

export = rootReducer;
