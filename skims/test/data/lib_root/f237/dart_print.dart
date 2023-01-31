import 'package:test/test.dart';

void main() {
  try {
    res = x ~/ y;
  }
  on IntegerDivisionByZeroException catch (e) {
    print(e);
    debugPrint(e);
  }
  catch (e) {
    print('This should not  be reported');
    debugPrint('Safe');
  }
}
