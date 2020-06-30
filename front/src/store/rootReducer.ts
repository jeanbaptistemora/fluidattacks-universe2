import { reducer as formReducer } from "redux-form";
import { Reducer, combineReducers } from "redux";

const rootReducer: Reducer = combineReducers({ form: formReducer });

export = rootReducer;
