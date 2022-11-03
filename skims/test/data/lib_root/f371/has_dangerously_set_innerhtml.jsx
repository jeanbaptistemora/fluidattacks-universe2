import React from "react";

const App = () => {
  const createMarkup = () => {
    return {
      __html: "<img onerror='alert();' src='invalid-image' />",
    };
  };
  return (
    <div>
      <div dangerouslySetInnerHTML={createMarkup()}/>
    </div>
  );
};
export default App;
