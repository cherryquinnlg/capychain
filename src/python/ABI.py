contract_abi = [
  {
    "constant": False,
    "inputs": [
      {
        "name": "_user",
        "type": "address"
      },
      {
        "name": "_time",
        "type": "string"
      },
      {
        "name": "_idHash",
        "type": "string"
      },
      {
        "name": "_reportHash",
        "type": "string"
      }
    ],
    "name": "addData",
    "outputs": [],
    "payable": False,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": False,
    "inputs": [
      {
        "name": "_users",
        "type": "address[]"
      },
      {
        "name": "_times",
        "type": "string[]"
      },
      {
        "name": "_idHashs",
        "type": "string[]"
      },
      {
        "name": "_reportHashs",
        "type": "string[]"
      }
    ],
    "name": "addDataBatch",
    "outputs": [],
    "payable": False,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": True,
    "inputs": [
      {
        "name": "_address",
        "type": "address"
      }
    ],
    "name": "getCountByUser",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": True,
    "inputs": [
      {
        "name": "_address",
        "type": "address"
      }
    ],
    "name": "getDataByUser",
    "outputs": [
      {
        "name": "",
        "type": "tuple[]"
      }
    ],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": True,
    "inputs": [
      {
        "name": "user",
        "type": "address"
      }
    ],
    "name": "getTimesByUser",
    "outputs": [
      {
        "name": "",
        "type": "string[]"
      }
    ],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": True,
    "inputs": [
      {
        "name": "user",
        "type": "address"
      },
      {
        "name": "time",
        "type": "string"
      }
    ],
    "name": "getIPFSByUserTime",
    "outputs": [
      {
        "name": "",
        "type": "string[]"
      }
    ],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
  }
]
