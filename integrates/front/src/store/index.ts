import type { Store } from "redux";
import { createStore } from "redux";
import rootReducer from "store/rootReducer";

const store: Store = createStore(rootReducer);

export = store;
