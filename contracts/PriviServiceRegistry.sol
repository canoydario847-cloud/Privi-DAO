// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @notice Governance-curated hashes/metadata references for Privi ecosystem services.
/// @dev Ownership should be transferred to the timelock only after governance review.
///      A registered service is not proof of deployment, authorization or health.
contract PriviServiceRegistry is Ownable {
    struct Service {
        string name;
        string metadataURI;
        bytes32 configurationHash;
        bool active;
        uint64 updatedAt;
    }

    mapping(bytes32 => Service) private services;

    event ServiceUpdated(bytes32 indexed serviceId, string name, string metadataURI, bytes32 configurationHash, bool active);

    constructor(address initialOwner) Ownable(initialOwner) {}

    function upsertService(
        bytes32 serviceId,
        string calldata name,
        string calldata metadataURI,
        bytes32 configurationHash,
        bool active
    ) external onlyOwner {
        require(serviceId != bytes32(0), "zero service id");
        require(bytes(name).length != 0 && bytes(name).length <= 128, "invalid name");
        require(bytes(metadataURI).length <= 2048, "URI too long");
        services[serviceId] = Service(name, metadataURI, configurationHash, active, uint64(block.timestamp));
        emit ServiceUpdated(serviceId, name, metadataURI, configurationHash, active);
    }

    function getService(bytes32 serviceId) external view returns (Service memory) {
        return services[serviceId];
    }
}
