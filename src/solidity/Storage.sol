// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract Storage {
    struct Data {
        address user;
        string time;
        string idHash;
        string reportHash;
    }

    Data[] public dataList;

    function addData(address _user, string memory _time, string memory _idHash, string memory _reportHash) public {
        Data memory newData = Data(_user, _time, _idHash, _reportHash);
        dataList.push(newData);
    }

    function addDataBatch(address[] memory _users, string[] memory _times, string[] memory _idHashs, string[] memory _reportHashs) public onlyOwner {
        for (uint256 i = 0; i < _users.length; i++) {
            Data memory newData = Data(_users[i], _times[i], _idHashs[i], _reportHashs[i]);
            dataList.push(newData);
        }

    }

    function getCountByUser(address _address) public view returns (uint256) {
        uint256 count = 0;
        for (uint256 i = 0; i < dataList.length; i++) {
            if (dataList[i].user == _address) {
                count++;
            }
        }
        return count;
        }

    function getDataByUser(address _address) public view returns (Data[] memory) {
        uint256 count = getCountByUser(_address);

        Data[] memory result = new Data[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < dataList.length; i++) {
            if (dataList[i].user == _address) {
                result[index] = dataList[i];
                index++;
            }
        }

        return result;
    }

    // Function to get all the times for a specific user
function getTimesByUser(address user) public view returns (string[] memory) {
        uint256 count = getCountByUser(user);

        string[] memory result = new string[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < dataList.length; i++) {
            if (dataList[i].user == user) {
                result[index] = dataList[i].time;
                index++;
            }
        }
        return result;
    }

    // Function to get all the times for a specific user
function getIPFSByUserTime(address user, string calldata time) public view returns (string[] memory) {
        uint256 count = getCountByUser(user);

        string[] memory result = new string[](count);
        uint256 index = 0;
        for (uint256 i = 0; i < dataList.length; i++) {
            if (dataList[i].user == user && keccak256(bytes(dataList[i].time)) == keccak256(bytes(time))) {
                result[index] = dataList[i].time;
                index++;
            }
        }
        return result;
    }
    }    