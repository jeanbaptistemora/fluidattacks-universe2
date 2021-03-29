// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
module.exports = (api) => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
  api.cache(true);

  return {
    env: {
      production: {
        plugins: ["react-native-paper/babel"],
      },
    },
    plugins: [["babel-plugin-inline-import", { extensions: [".svg"] }]],
    presets: ["babel-preset-expo"],
  };
};
