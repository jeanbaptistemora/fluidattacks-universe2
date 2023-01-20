const safeObj2 = {
  attr: "val",
  key1: "val1",
};

// strings storage is allowed
localStorage.setItem("anyKey", "anyStringValue");

// JSON.parse usage with safe objs:
localStorage.setItem("anyKey", JSON.stringify(safeObj2));
