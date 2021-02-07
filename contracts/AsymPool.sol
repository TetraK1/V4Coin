// SPDX-License-Identifier: MIT

pragma solidity ^0.8.1;

import "./ERC20.sol";

contract AsymPool is ERC20 {
    address public creator;
    bool isInitialized = false;
    address public token0;
    address public token1;

    uint private reserve0;
    uint private reserve1;

    uint private peg;

    constructor () {
        creator = msg.sender;
    }

    function initialize(address _token0, address _token1) external {
        require(msg.sender == creator);
        token0 = _token0;
        token1 = _token1;
        isInitialized = true;
    }

}
