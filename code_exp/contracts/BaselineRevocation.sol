// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title BaselineRevocation
 * @dev A simple, baseline smart contract for managing certificate revocations.
 * This contract uses a basic mapping to store the revocation status of each certificate.
 * It serves as a performance and cost baseline to compare against more advanced
 * revocation mechanisms (e.g., those using cryptographic accumulators).
 */
contract BaselineRevocation {
    // Mapping from a certificate ID to its revocation status.
    // `true` means the certificate is revoked.
    mapping(bytes32 => bool) public revoked;

    address public owner;

    event CertificateRevoked(bytes32 indexed certificateId);

    constructor() {
        owner = msg.sender;
    }

    /**
     * @dev Revokes a certificate.
     * Only the owner of the contract can call this function.
     * @param certificateId The unique identifier of the certificate to revoke.
     */
    function revoke(bytes32 certificateId) external {
        require(msg.sender == owner, "Only owner can revoke.");
        require(!revoked[certificateId], "Certificate already revoked.");
        
        revoked[certificateId] = true;
        emit CertificateRevoked(certificateId);
    }

    /**
     * @dev Checks if a certificate is revoked.
     * @param certificateId The unique identifier of the certificate to check.
     * @return bool Returns true if the certificate is revoked, false otherwise.
     */
    function isRevoked(bytes32 certificateId) external view returns (bool) {
        return revoked[certificateId];
    }
}
