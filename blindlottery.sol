pragma solidity ^0.4.22;

contract blindLottery{
        address public owner;
        uint public numplayed=0;
        uint256 public winning_number;
        mapping(address => bytes32)public hashes;
        address[] winners;
        uint public numwin;
        
        constructor () public {
            owner =msg.sender;
        }
        event played(address player, bytes32 h);
        function play (bytes32 h) external payable {
                if (add_player(msg.sender)){
                        require( msg.value == 100 finney);
                        hashes[msg.sender]=h;
                        emit played(msg.sender, h);

        }}
        function finish (uint256 winning_number_) external {
                require(msg.sender == owner);
                winning_number = winning_number_;
                
        }
        function  claim (uint256 r) external{
            bytes32 hash = sha256(winning_number,r);
            require (hashes[msg.sender] == hash);
            winners[numwin]=msg.sender;
            numwin++;
        }

        function add_player (address player) private returns (bool){
                require(msg.sender!=owner);
                if (hashes[player]!=0){ return false;}
                assert (hashes[player]==0);
                numplayed+=1;
                return true;
}
        function finalize () external{
            uint256 balanceend = address(this).balance;
            uint256 tax = balanceend/20;
            uint256 rest = balanceend - tax;
            owner.transfer(tax);
            for (uint256 x=0;x<=numwin;x++){
                winners[x].transfer(rest/numwin);
            }
        selfdestruct(owner);
        }
}
