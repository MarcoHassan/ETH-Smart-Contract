pragma solidity ^0.4.22;


contract lower_Weather_transfer 

    {

    function temperature_send(address _receiver,
        	              int256 temperature, int256 apparent) public payable
			  {
			  assert(temperature <= apparent);
			  require(msg.value <= msg.sender.balance, "Insufficient balance.");
			  _receiver.transfer(msg.value);
			  }
    }
			

contract higher_Weather_transfer 

    {
    function temperature_send(address _receiver,
        	              int256 temperature, int256 apparent) public payable
			  {
			  assert(temperature > apparent);
			  require(msg.value <= msg.sender.balance, "Insufficient balance.");
			  _receiver.transfer(msg.value);
			  }
    }
		