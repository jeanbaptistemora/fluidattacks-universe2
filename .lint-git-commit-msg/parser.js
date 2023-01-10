module.exports = {
  parserOpts: {
    headerPattern:
      /^(airs|all|asserts|common|docs|integrates|melts|observes|reviews|skims|sorts|teaches)\\(\w*)\((\w*)\):\s(#[1-9]\d*)\s(.*)$/,
    headerCorrespondence: ["product", "type", "scope", "ticket", "subject"],
  },
};
