module.exports = (api) => {
  api.cache(true);

  return {
    env: {
      production: {
        plugins: ["react-native-paper/babel"],
      },
    },
    plugins: [["babel-plugin-inline-import", { "extensions": [".svg"] }]],
    presets: ["babel-preset-expo"],
  };
};
