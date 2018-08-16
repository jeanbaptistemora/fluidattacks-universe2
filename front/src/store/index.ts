import { createStore } from "redux";
import rootReducer from "./rootReducer";

const store: typeof rootReducer = createStore(rootReducer);
export = store;
