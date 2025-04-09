{
  "type": "CMD_LIST",
  "body": [
    {
      "type": "IF",
      "cond": {
        "type": "BIN_OP",
        "op": "+",
        "left": {
          "type": "ID",
          "name": "x"
        },
        "right": {
          "type": "NUMBER",
          "value": 2
        }
      },
      "body": {
        "type": "CMD_LIST",
        "body": [
          {
            "type": "RETURN",
            "value": {
              "type": "ID",
              "name": "x"
            }
          }
        ]
      }
    },
    {
      "type": "ASSIGN",
      "var": "y",
      "op": "=",
      "value": {
        "type": "NUMBER",
        "value": 5
      }
    },
    {
      "type": "RETURN",
      "value": {
        "type": "BIN_OP",
        "op": "+",
        "left": {
          "type": "ID",
          "name": "y"
        },
        "right": {
          "type": "NUMBER",
          "value": 1
        }
      }
    }
  ]
}
