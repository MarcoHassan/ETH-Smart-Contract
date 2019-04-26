pragma solidity ^0.5.7;

contract Greeter {
    bytes32 public greeting;

    function greeter() public {
        greeting = 'Hello';
    }

    function setGreeting(bytes32 greetin) public {
        greeting = greetin;
    }

    function greet() view public returns (bytes32) {
        return greeting;
    }
}