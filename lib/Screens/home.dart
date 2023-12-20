import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<Home> {
  final TextEditingController _controller = TextEditingController();
  final _channel = WebSocketChannel.connect(
    Uri.parse("ws://localhost:8765"),
  );

  Map<int, int> whiteMidiIdxs = {
    0: 36,
    1: 38,
    2: 40,
    3: 41,
    4: 43,
    5: 45,
    6: 47,
    7: 48,
    8: 50,
    9: 52,
    10: 53,
    11: 55,
    12: 57,
    13: 59,
    14: 60,
    15: 62,
    16: 64,
    17: 65,
    18: 67,
    19: 69,
    20: 71,
    21: 72,
    22: 74,
    23: 76,
    24: 77,
    25: 79,
    26: 81,
    27: 83,
    28: 84,
    29: 86,
    30: 88,
    31: 89,
    32: 91,
    33: 93,
    34: 95,
    35: 96
  };
  Map<int, int> blackMidiIdxs = {
    1: 37,
    3: 39,
    5: 42,
    7: 44,
    9: 46,
    12: 49,
    14: 51,
    16: 54,
    18: 56,
    20: 58,
    23: 61,
    25: 63,
    27: 66,
    29: 68,
    31: 70,
    34: 73,
    36: 75,
    38: 78,
    40: 80,
    42: 82,
    45: 85,
    47: 87,
    49: 90,
    51: 92,
    53: 94
  };
  Map<String, Color> colorMap = {
    "blue": Colors.blue,
    "red": Colors.red,
    "green": Colors.green,
    "yellow": Colors.yellow
  };

  Color getColor(int i, var note2color, {bool isWhite = true}) {
    Map<int, int> whiteMidiIdxs = {
      0: 36,
      1: 38,
      2: 40,
      3: 41,
      4: 43,
      5: 45,
      6: 47,
      7: 48,
      8: 50,
      9: 52,
      10: 53,
      11: 55,
      12: 57,
      13: 59,
      14: 60,
      15: 62,
      16: 64,
      17: 65,
      18: 67,
      19: 69,
      20: 71,
      21: 72,
      22: 74,
      23: 76,
      24: 77,
      25: 79,
      26: 81,
      27: 83,
      28: 84,
      29: 86,
      30: 88,
      31: 89,
      32: 91,
      33: 93,
      34: 95,
      35: 96
    };
    Map<int, int> blackMidiIdxs = {
      1: 37,
      3: 39,
      5: 42,
      7: 44,
      9: 46,
      12: 49,
      14: 51,
      16: 54,
      18: 56,
      20: 58,
      23: 61,
      25: 63,
      27: 66,
      29: 68,
      31: 70,
      34: 73,
      36: 75,
      38: 78,
      40: 80,
      42: 82,
      45: 85,
      47: 87,
      49: 90,
      51: 92,
      53: 94
    };

    Map<String, Color> colorMap = {
      "blue": Colors.blue,
      "red": Colors.red,
      "green": Colors.green,
      "yellow": Colors.yellow
    };

    if (isWhite) {
      return colorMap[note2color[whiteMidiIdxs[i].toString()]] ?? Colors.white;
    } else {
      return colorMap[note2color[blackMidiIdxs[i].toString()]] ?? Colors.black;
    }
  }

  Widget _pianoKeys(var note2Color) {
    List<Widget> whiteKeys = [];
    for (int i = 0; i < 36; i++) {
      Container key = Container(
        height: 180,
        width: 30,
        decoration: BoxDecoration(
            color: getColor(i, note2Color, isWhite: true),
            border: Border.all(color: Colors.black, width: 1)),
      );
      whiteKeys.add(key);
    }

    const SizedBox blank = SizedBox(height: 100, width: 15);
    const SizedBox bigBlank = SizedBox(height: 100, width: 22.5);
    const SizedBox hugeBlank = SizedBox(height: 100, width: 45);

    List<Widget> blackSet = [];
    for (int i = 0; i < 55; i++) {
      int idx = i % 11;
      if (idx == 0 || idx == 10) {
        blackSet.add(bigBlank);
      } else if (idx == 2 || idx == 6 || idx == 8) {
        blackSet.add(blank);
      } else if (idx.isOdd) {
        blackSet.add(Container(
          height: 100,
          width: 15,
          decoration: BoxDecoration(
              color: getColor(i, note2Color, isWhite: false),
              border: Border.all(color: Colors.black, width: 1)),
        ));
      } else {
        blackSet.add(hugeBlank);
      }
    }

    return Stack(
      children: [
        Row(
          mainAxisSize: MainAxisSize.min,
          children: whiteKeys,
        ),
        Row(
          mainAxisSize: MainAxisSize.min,
          children: blackSet,
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Davenport"),
      ),
      body: StreamBuilder(
          stream: _channel.stream,
          builder: (context, snapshot) {
            var data = {};
            if (snapshot.hasData) {
              String text = String.fromCharCodes(snapshot.data);
              print(text);
              data = json.decode(text);
            }
            return Center(
              child: Column(
                children: [
                  FittedBox(child: _pianoKeys(data["key_data"] ?? {})),
                  Text(
                    data["prompt"] ?? "",
                    style: const TextStyle(fontSize: 128),
                  ),
                  Text(
                    data["message"] ?? "", style: TextStyle(fontSize: 42),
                  )
                ],
              ),
            );
          }),
    );
  }
}
