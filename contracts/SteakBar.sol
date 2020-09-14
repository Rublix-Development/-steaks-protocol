pragma solidity 0.6.12;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/math/SafeMath.sol";


contract SteakBar is ERC20("SteakBar", "xSTEAK"){
    using SafeMath for uint256;
    IERC20 public steak;

    constructor(IERC20 _steak) public {
        steak = _steak;
    }

    // Enter the bar. Pay some STEAK. Earn some shares.
    function enter(uint256 _amount) public {
        uint256 totalSteak = steak.balanceOf(address(this));
        uint256 totalShares = totalSupply();
        if (totalShares == 0 || totalSteak == 0) {
            _mint(msg.sender, _amount);
        } else {
            uint256 what = _amount.mul(totalShares).div(totalSteak);
            _mint(msg.sender, what);
        }
        steak.transferFrom(msg.sender, address(this), _amount);
    }

    // Leave the bar. Claim back your STEAK.
    function leave(uint256 _share) public {
        uint256 totalShares = totalSupply();
        uint256 what = _share.mul(steak.balanceOf(address(this))).div(totalShares);
        _burn(msg.sender, _share);
        steak.transfer(msg.sender, what);
    }
}
