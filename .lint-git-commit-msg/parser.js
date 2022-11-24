module.exports = {
  parserOpts: {
    headerPattern: /^(airs|all|asserts|common|docs|forces|integrates|melts|observes|reviews|skims|sorts|teaches)\\(\w*)\((\w*)\):\s(#[1-9]\d*)(.\d+)?\s(.*)$/,
    headerCorrespondence: [ 'product', 'type', 'scope', 'ticket', 'part', 'subject' ],
  },
};
