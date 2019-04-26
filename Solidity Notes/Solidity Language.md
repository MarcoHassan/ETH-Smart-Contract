# Ethereum & Solidity

Smart contracts are written in Solidity but the machine to execute a contract does not understand Solidity so hte code must be translated ot something which can be understood on the Ethereum network.

This is the job of the solidity compiler that similarly to a C++ compiler transform the human-readable language to machine-readable language - in the Ethereum Network - EWM.

## Data types

Common. Similar to C++. If you have any doubts refer to this link [Solidity Language](https://solidity.readthedocs.io/en/v0.5.7/types.html).

An interesting data type is ```address```. This refers to an Ethereum Adress.
An ```address``` can be of two types: ```address payable``` or simply ```address```. This will be important as you will be able to send money to an ```address payable``` while you will not be able to do so to a simple ```address```.

Also functions can be of different types. They can be ```payable/non-payable``` ```pure``` or of ```view``` type.

```pure``` and ```view```  functions are functions, that are promised not to modify or read the state.
In detail this function will not perform the following functions:
(i)    State variables being written to.
(ii)   Events being emitted.
(iii)  Other contracts being created.
(iv)   selfdestruct being used.
(v)    Ether being sent via calls.
(vi)   Calling functions that are not marked view or pure.
(vii)  Low-level calls being used.
(viii) Inline assembly containing certain opcodes being used
In addition to the above ```pure``` functions will be restricted by the fact that their value will only depends on the function arguements.
In simple terms use the following rule of thumbs: use ```view``` if the funcition will not alter the storage state in any way. Use ```pure``` if the function won't even read the storage state.

Payable functions also accepts a payment of zero Ethereum so basically it can be implicitely of type ```non-payable```, the same does not apply to ```non-payable``` functions, where if a function tries to carry out a transaction it is rejected.

Notice that ```public``` or ```external``` functions have the following member functions:

       1. ```.selector```, this returns the ABI function selector.

       2. ```.gas(unit)```, this returns a callable function object which, when called, will send the specified amount of gas to the targer funciton.

       3. ```.value(uint)``` this returns a callable function object which, when called, will send the specified amount of wei to the targer function.

## Data Location

As in C++ when you create certain types such as ```arrays``` or ```structs``` you must provide the location where these are stored. There are three types of data locations:

   1. ```memory```

   2. ```storage```

   3. ```calldata```, this is a non-modifiable, non-persistent area where function arguments are stored and behaves mostly like memory. 

## Mapping types

Mappings are used to save key-value pairs. In the specific the key-data entered is not saved in the mapping but rather its kecak256 hash is.

In general it is possible to save a mapping in the following way:
	    
```
pragma solidity ^0.4.0;

contract exampleMapping {
    mapping(address => uint) public balances;

    function update(uint balanceNew) {
        balances[msg.sender] = balanceNew;
    }
}

contract userMapping {
    function f() returns (uint) {
        exampleMapping m = new exampleMapping();
        m.update(100);
        return m.balances(this);
    }
}
```

What mappings do in the specific is to assign to each key a unique
value (in this case an unsigned integer) in order to withdrew the
key. At the same time when declaring a map a getter function is
created. This allows to allows to call the data related to the key as
in the example above. There you get the balance amount by the key, in
the case the sender address. By referencing the specified mapping
balances together with its key you have access to elements specified
within it.

Notice that while you are restricted in the key type as this cannot be
a ```struct```, ```mapping```, ```enum```, ```dynamic array``` or ```contract``` the same does not hold true for the ```value```
pair. This can be of either type and even a mapping in which case the value is dynamically evaluated by going through all of the mapping series.
   

## Time units

You have simeple suffixes that will let you manage time objects in a simple way.
In the specific you will have the ```seconds```, ```minutes```, ```hours```, ```days``` and ```weeks``` to call any of these suffixes.

To make the point clear think of the following function:

   ```
function f(uint start, uint daysAfter) public {
    if (now >= start + daysAfter * 1 days) {
      // ...
    }
}
```

## Send Messages

This is done through Solidity's ```call``` function. This is a
low-level interface for sending a message to a contract. For intance
it is easy to send a ```bytes``` array containing stringliterals to a
contract by using the following code: ```<contract>.call("string")```.

## Important Block and Transaction Calls

```blockhash(unit blockNumber) returns(bytes32)```: returns the hash of the given block.

```block.gaslimit(uint)```: returns current block gaslimit.

```block.timestamp(uint)```: current block timestamp as seconds since unix epoch.

```gasleft() returns(uint256)```: remaining gas.

```msg.data(bytes calldata)```: returns calldata, that is where the functions arguments are saved.

```msg.sender (address payable)```: returns sender of the current call.

```now(unit)```: current timestamp. This is an alias for ```block.timestamp```.

```msg.value (uint)```: returns the number of Ethereum coins sent with the message.

## Member functions of Address Types

```<address>.balance (uint256)```: returns the balance of the Address in Ethereum Coins.

```<address payable>.transfer(uint256 amount)```: send a given amount of Ethereum coins to an Address, reverts on failure.

```this```: returns the current contract.

```selfdestruct(address payable recipient)```: destroys the current contract, sending its funds to the given address.

## Conditions and error messages

```assert(bool condition)```: when the bool condition does not hold to be true all of the gas is consumed and the entire contract terminates undoing all the state changes.

```require(bool condition)```: this is more forgiving. When the require statement is not met the contract does not abort and terminates but rather throws an error message is called and the contract continues.

So in general ```assert()``` is used just to prevent something really bad from happening. In contrast ```require()``` should be your function for checking conditions for conditional contracts.

## Type information of the contract

```type(x).name```: returns the name of the contract X.

```type(x).creationCode```: returns the byte array with the creation byteccode of the contract.

## Calling function on a contract

This can be done by calling ```<contract>.function```. Notice however that the function will be interpreted as an external function.

It is moreover possible to send a given amount of gas and a specific value of Ethereum coins with a function. This is done calling the following command.

```
feed.info.value(5).gas(200)()
notice the () at the end as calling the function without them will not execute it and the value and gas settings passed will be lost.
```

## Create contracts in contracts.

It is possible to create a contract while executing another making user of the ```new``` operator.

See the following code for instance:

```
pragma solidity >=0.5.0 <0.7.0;

contract D {
    uint public x;
    constructor(uint a) public payable {
        x = a;
    }
}

contract C {
    D d = new D(4); // will be executed as part of C's constructor

    function createD(uint arg) public {
        D newD = new D(arg);
        newD.x();
    }

    function createAndEndowD(uint arg, uint amount) public payable {
        // Send ether along with the creation
        D newD = (new D).value(amount)(arg);
        newD.x();
    }
}
```


## Contracts

Contracts in solidity are very similar to classes in OOP.

As in C++ you have different wazs to specify functions within a contract. Functions can be:

1. ```external```: this means that they are generally accessible, even from other contracts (read classes). External functions cannot be called internally but have always to referencce the contract they refer to. For instance, given an external function ```fun```, you will not be able  to call it internally in the contract  by calling ```fun``` but you will have rather to call it by evoquing the contract, i.e. calling ```this.fun```.

2. ```public``` : these are functions that are part of the contract interface and can be either called ```internally``` or via ```messages```. Notice that in case of ```pulic state VARIABLS``` an automatic getter function is automatically generated so that the value of the variables is generally accessible. Getter funcitons will then operate by ```<contract>.get<public state variable>()```.

3. ```internal```: these are functions that can only be accessed internally in the given contract. It follows that inovquing such function by calling ```this.<fucnction>``` will be erroneous.

4. ```private```: these are just visible for the contract they are defined in and not for derived contracts.

_Important_: notice the difference with C++. The private and internal specifications will not affect visibility of the user. Everything that is inside of a contract will be visible to external observers. So the difference lies not in the strict visibility but rather in the accessability of the function to other contracts.

#### Specify derived contract

To specify a derived contract use the following syntax:

```
contract newContract is originContract{...}
```

## Function Modifiers

Modifiers can be used to easily change the behaviour of
funcitons. They are usually used to check for a condition prior to
executing the function. 

In general after defining a modifier you will insert a wildcard
```_;``` within it. When a function is specified inheriting such
modifier function it will then execute in the place where the wildcard
is displayed.

More formally, to illustrate the usage of modifiers let's look at the following
example.


**Case 1: Inside a Contract**

``` 
pragma solidity ^0.4.18;

contract underscore {
    uint public a;
    constructor() public { 
        a = 10;
    }
    
    modifier conditionalChangeAtoThirty() {
        _;
        if (a == 20){
            a = 30;
        }
    }
    
    function changeaToTwenty() 
        public 
        conditionalChangeAtoThirty
    {
        a = 20;
    }
}
```

Above you have defined the modifier ```conditionalChangeAtoThirty()```
This is passed to the function ```changeaToTwenty()```.

What will happen thus is that the function changeToTwenty will be
passed to the wildcard in the modifier function and the two functions
will run together as a one. Depending then on the place of the
wildcard the function invoquing the modifier function will execute
before or later.

_Notice_ how such modifier functions are especially useful for
executing conditional contracts. To see this check at the following
example:

```
modifier onlySeller() {
    require(
        msg.sender == seller,
        "Only seller can call this."
    );
    _;
}
```

_Final Note_: it is important to remember that there can be multiple
wildcards into a modifier function so that the function invoquing the
latter can take multiple positions into the modifier.


**Case 2 - Implicitely by calling a Contract containing a modifier**

It is important to remeber that referring directly a modifier function
such in **Case 1** is not the only viable option. It is in fact also
possible to pass a modifier functin by passing to function a _contract
containing a modifier function_.

To understand this think about the following example:

```
pragma solidity >=0.5.0 <0.7.0;

contract owned {
    constructor() public { owner = msg.sender; }
    address payable owner;

	modifier onlyOwner {
        require(
            msg.sender == owner,
            "Only owner can call this function."
        );
        _;
    }
}

contract mortal is owned {
    // This contract inherits the `onlyOwner` modifier from
    // `owned` and applies it to the `close` function, which
    // causes that calls to `close` only have an effect if
    // they are made by the stored owner.
    function close() public onlyOwner {
        selfdestruct(owner);
    }
}
```

## Return Specification of Functions

Differently from other langugages you know Solidity requires you to
specify the rutn types of variables if the function will return
anything. 

This means that when specifying the function you should also specify
the return type as an argument of the function. 

Check at the following example for instance

```
pragma solidity >=0.4.16 <0.7.0;

contract Simple {
    function arithmetic(uint a, uint b)
        public
        pure
        returns (uint osum, uint oproduct) // this must be specified
			                                 // when defyining the function.
    {
        osum = a + b;
        oproduct = a * b;
    }
}
```

_Notice_: that it is not necessary to specify the names of the variables
that will be returned. 

_Notice_: it is not possible to return structs or arrays with the
current version of the compiler 0.5.4. In order to do so you have to
add the beta version of the ABIEncoder by adding at the beginning ```pragma experimental ABIEncoderV2;```.

_Notice_: In the above example you do not need to specify a second
type the return entry when you want to return your type. This is
because that was already specified in the above ```returns```
statement. An alternative would rely on not evoquing neither osum, nor
oproduct at the end but rather returning the operations themeself in
the following way:

```
pragma solidity >=0.4.16 <0.7.0;

contract Simple {
    function arithmetic(uint _a, uint _b)
        public
        pure
        returns (uint o_sum, uint o_product)
    {
        return (_a + _b, _a * _b);
    }
}
```

Please remember notheless that in the above case the ```return``` must
be specified.

## Fallback Function

Each contract can hold max **one** ```fallback function```. This is a
function that has no arguments and does not return anything. Moreover
it has to have external visibility.

This funcition is then executed whenever a call is made to the
contract if none other function matches the given function modifier or
when no data is supplied at all.

Moreover it is possible to make use of such a funciton to store
received Ether when these are sent without data. It is important
nonetheless ot specify the cllback function being of ```payable```
type.

Notice that the ```fallback function``` is supplied with 2300 units of
gas. This means that just some basics functions can be performed with
the ```fallback function``` before defining it, it is therefore
advisable to checck the number of gas required to perfom the
computation by the function.

_Notice_: Despite the fact that the ```fallback function``` cannot
hace any arguments, it can still accept the ```msg.data``` to retrieve
the data sent within a message - for instance the Ethereum sent -.

Notice that especially when using the ```fallback function``` to
receive Ethers you should make sure to just execute the fallback when
Ether are sent and not when a function called does not exist. In order
to insure such a behaviour it is possible to set a ```require```
clause in the follwing way: ```require(msg.data.length == 0)```.

_Example_:

```
pragma solidity ^0.4.0;

contract TestContract {
    // The function below will be called for each message
    // that is sent to this contract (as there is no other function to call).
    // However, if Ether is sent to this contract, an exception will occur.
    // That is because this contract does not have the "payable" modifier.
    function() { a = 1; }
    uint a;
}


// this is a contract, which keeps all Ether to it with not way of 
// retrieving it.
contract SinkContract {
    function() payable { }
}

contract CallerContract {
    function testCall(TestContract test) {
        test.call(0xabcdef01); // hash is non-existent
        // will result in test.a becoming == 1.

        // The following statement is not going to compile.
        // But if ether is sent to this contract, the
        // transaction would fail and the Ether would be rejected
        //test.send(2 ether);
    }
}
```


## Events

Solidity allows to make use of events data structures that creates **EVM
logs** that will be stored on the transaction's log on the
blockchain. These logs are associated with the contract's address and
are to be incorporated into the blockchain itself to stay there as
long the block is acessible. 

This is moreover useful for Dapps where it Javascripts callbacks might
call such EVM logs.

## Abstract Contracts

It is sometimes useful to create **base contracts**. These are
contracts that cannot be compiled by themselve because they **lack
function implementation**. 

This means that such contracts are not intended to be implemented
themself but rather as a base for other kind of contracts. 

What is done is therefore to write an ```abstract contract``` stating
the functionality of a contract and letting a second contract be
derived from such defined abstract contract. In such a way you will
**force** the derived contract to have the same structure as the
abstract one and to have **function implementations** for the
not-specified functions of ```abstract contracts```. If a derived
contract will also lack **function implementation** it will still be
an ```abstract contract```.

 Abstract contracts are in this sense very much intended as methods to define contracts without implementing them. The implementation will just take place at a later stage.

## Interfaces
	
Interfaces are similar to abstract contracts, but they cannot have any functions implemented. There are further restrictions:

(i)   They cannot inherit other contracts or interfaces.
(ii)  All declared functions must be external.
(iii) They cannot declare a constructor.
(iv)  They cannot declare state variables.
(v)   Some of these restrictions might be lifted in the future.
	
Interfaces are denoted by their own keyword:	

```
pragma solidity >=0.5.0 <0.7.0;

interface Token {
    enum TokenType { Fungible, NonFungible }
    struct Coin { string obverse; string reverse; }
    function transfer(address recipient, uint amount) external;
}
```
