import 'dart:io';
import 'package:logging/logging.dart';

class Test {
  static final logger = Logger('Test');

  void insecure1(HttpRequest req, HttpResponse resp) {
    String param1 = req.uri.queryParameters['param'];
    logger.info('Param1: $param1'); // Insecure
  }

  void insecure2(HttpRequest req) {
    String param = req.headers.value('header');
    logger.severe('Dangerous: $param'); // Insecure
  }

  void safe(HttpRequest req) {
    String param2 = req.uri.queryParameters['param2'];
    param2 = param2.replaceAll(RegExp("[\n\r\t]"), '_'); // Sanitize parameter
    logger.info('Param1: $param2'); // Safe
  }
}
