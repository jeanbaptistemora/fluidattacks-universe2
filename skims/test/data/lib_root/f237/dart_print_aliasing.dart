import 'package:test/test.dart' as my_alias;
import 'package:flutter/foundation.dart' as anyAlias;
import 'dart:developer' as dev;

void main() {
  try {
    res = x ~/ y;
  }
  on IntegerDivisionByZeroException catch (e) {
    // Following lines should be reported
    dev.log(e);
    anyAlias.debugPrint(e);

    // Coming lines Should not be reported
    log(e);
    debugPrint(e);
  }
  catch (e) {
    print('This should not  be reported');
    debugPrint('Safe');
  }
}
