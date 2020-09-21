module.exports = {
  parserOpts: {
    headerPattern: /^(airs|all|asserts|common|forces|integrates|observes|reviews|serves|skims|sorts|melts|teaches)\\(\w*)\((\w*)\):\s(#[1-9]\d*)(.\d+)?\s(.*)$/,
    headerCorrespondence: [ 'product', 'type', 'scope', 'ticket', 'part', 'subject' ],
  },
};
