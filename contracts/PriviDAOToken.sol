// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Permit} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Permit.sol";
import {ERC20Votes} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
import {Nonces} from "@openzeppelin/contracts/utils/Nonces.sol";

/// @notice Distinct governance token for Privi DAO on Base, NOT native PRVI or PRIV.
/// @dev One-time fixed supply. No owner, minting, transfer tax, pause or blacklist.
contract PriviDAOToken is ERC20, ERC20Permit, ERC20Votes {
    uint256 public constant INITIAL_SUPPLY = 1_000_000_000 ether;

    constructor(address initialRecipient)
        ERC20("Privi DAO Governance", "PDAO")
        ERC20Permit("Privi DAO Governance")
    {
        require(initialRecipient != address(0), "recipient required");
        _mint(initialRecipient, INITIAL_SUPPLY);
    }

    function _update(address from, address to, uint256 value)
        internal override(ERC20, ERC20Votes)
    {
        super._update(from, to, value);
    }

    function nonces(address owner)
        public view override(ERC20Permit, Nonces) returns (uint256)
    {
        return super.nonces(owner);
    }
}
