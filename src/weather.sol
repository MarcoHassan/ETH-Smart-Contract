pragma solidity ^0.4.22;

contract Weather_transfer {
    // The keyword "public" makes those variables
    // easily readable from outside.
    address public sender;
    mapping (address => uint) public balances;

    function temperature_send(address receiver, uint amount,
        	              int256 temperature, int256 apparent) public
			  {
			  if (temperature <= apparent)
			     {
     		      require(amount <= balances[msg.sender], "Insufficient balance.");
			      balances[msg.sender] -= amount;
			      balances[receiver] += amount;
			     } else
			     {
     			  require(amount <= balances[receiver], "Insufficient balance.");
			      balances[receiver] -= amount;
			      balances[sender] += amount;
			     }
			  }
}

