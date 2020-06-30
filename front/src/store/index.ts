import rootReducer from "./rootReducer";
import { Store, createStore } from "redux";

const store: Store = createStore(rootReducer);

export = store;
