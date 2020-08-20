module.exports = {
  parserOpts: {
    headerPattern: /^(all|forces|integrates|reviews|serves|skims|sorts)\\(\w*)\((\w*)\):\s(#[1-9]\d*)(.\d+)?\s(.*)$/,
    headerCorrespondence: [ 'product', 'type', 'scope', 'ticket', 'part', 'subject' ],
  },
};
