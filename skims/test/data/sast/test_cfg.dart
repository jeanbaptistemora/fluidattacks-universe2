import 'dart:math';
import 'package:test/test.dart';

var name = 'Voyager I';
var year = 1977;
var antennaDiameter = 3.7, radius = 1.8;
var flybyObjects = ['Jupiter', 'Saturn', 'Uranus', 'Neptune'];
var halogens = {'fluorine', 'chlorine', 'bromine', 'iodine', 'astatine'};
var names = <String>{};
var image = {
  'tags': ['saturn'],
  'url': '//path/to/saturn.jpg'
};
var gifts = Map<String, String>();
var visibility = isPublic ? 'public' : 'private';
var p1 = new Point(2, 2);


const oneSecond = Duration(seconds: 1), twoSeconds = Duration(seconds: 2);
const Object i = 3;
const list = [i as int];
const map = {if (i is int) i: 'int'};
const myset = {if (list is List<int>) ...list};

late String description;
final String nickname = 'Bobby';
enum Status {
   none,
   running,
   stopped,
   paused
}

class ImmutablePoint {
  static const ImmutablePoint origin = ImmutablePoint(0, 0);
  final double x, y;
  const ImmutablePoint(this.x, this.y);

  static double distanceBetween(Point a, Point b) {
    var dx = a.x - b.x;
    var dy = a.y - b.y;
    return sqrt(dx * dx + dy * dy);
  }
}

Iterable<int> naturalsTo(int n) sync* {
  int k = 0;
  while (k < n) yield k++;
}

class SmartTelevision extends Television {
  void turnOn() {
    super.turnOn();
    _bootNetworkInterface();
    _initializeMemory();
    _upgradeApps();
  }
}

class Musician extends Performer with Musical {
  // ···
}

class Spacecraft {
  String name;
  DateTime? launchDate;
  int? get launchYear => launchDate?.year;

  Spacecraft(this.name, this.launchDate) {
    print("Hello SpaceCraft");
  }

  @override
  bool operator == (Object other) => other is Vector && x == other.x && y == other.y;

  void describe() {
    print('Spacecraft: $name');
    var launchDate = this.launchDate;
    if (launchDate != null) {
      int years = DateTime.now().difference(launchDate).inDays ~/ 365;
      print('Launched: $launchYear ($years years ago)');
    } else {
      print('Unlaunched');
    }
  }
}

void main() {
  // Control structures
  if (year >= 2001) {
    print('21st century');
  } else if (year >= 1901) {
    print('20th century');
  }

  for (final object in flybyObjects) {
    print(object);
  }

  for (int month = 1; month <= 12; month++) {
    print(month);
  }

  for (int i = 0; i < candidates.length; i++) {
    var candidate = candidates[i];
    if (candidate.yearsExperience < 5) {
      continue;
    }
    if (candidate.yearsExperience > 7) {
      break;
    }
    candidate.interview();
  }

  while (year < 2016) {
    year += 1;
  }

  do {
    printLine();
  } while (!atEndOfPage());

  int fibonacci(int n) {
    if (n == 0 || n == 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
  }

  flybyObjects.where((name) => name.contains('turn')).forEach(print);

  switch ( expression ) {
    case value1: {
      print("Value $value1");
    } break;
    case value2: {
      print("Value $value2");
    } break;
    default: {
      print("Default case");
    } break;
  }

  if (astronauts == 0) {
    throw StateError('No astronauts.');
  }

  gifts['first'] = 'partridge';

  String piAsString = 3.14159.toStringAsFixed(2);
  assert(piAsString == '3.14');

  try {
    res = x ~/ y;
  }
  on IntegerDivisionByZeroException {
    print('Cannot divide by zero');
  }
  on EspecialException  catch (e) {
    print('Especial exception $e');
    rethrow;
  }
  catch(e) {
    print(e);
  }
  finally {
    print('Finally block executed');
  }
}

Future<void> createDescriptions(Iterable<String> objects) async {
  for (final object in objects) {
    try {
      var file = File('$object.txt');
      if (await file.exists()) {
        var modified = await file.lastModified();
        print('File for $object already exists. It was modified on $modified.');
        continue;
      }
      await file.create();
      await file.writeAsString('Start describing $object in this file.');
    } on IOException catch (e) {
      print('Cannot create description for $object: $e');
    }
  }
}


bool isNoble(int atomicNumber) {
  (employee as Person).firstName = 'Bob';
  var paint = Paint()
    ..color = Colors.black
    ..strokeCap = StrokeCap.round
    ..strokeWidth = 5.0;


  return _nobleGases[atomicNumber] != null;
}

String say(String from, String msg, [String? device]) {
  var result = '$from says $msg';
  if (device != null) {
    result = '$result with a $device';
  }
  return result;
}

const list = ['apples', 'bananas', 'oranges'];
list.map((item) {
  return item.toUpperCase();
}).forEach((item) {
  print('$item: ${item.length}');
});

Function makeAdder(int addBy) {
  if ((n % i == 0) && (d % i == 0)) {
    a = 0;
    b = ++a;
    return (int i) => addBy + i;
  }
}
