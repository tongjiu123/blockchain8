// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/structs/EnumerableSet.sol";

/**
 * @title Certificate
 * @dev This contract manages the lifecycle of academic certificates using a hybrid storage model.
 * It stores a hash of the certificate data on-chain, while the full data is stored off-chain (e.g., IPFS).
 * This approach significantly reduces gas costs and improves scalability.
 */
contract Certificate is Ownable {
    using EnumerableSet for EnumerableSet.AddressSet;

    // --- Events ---
    event CertificateIssued(bytes32 indexed certificateHash, address indexed institution, uint256 timestamp);
    event CertificateRevoked(bytes32 indexed certificateHash, address indexed institution, uint256 timestamp);
    event InstitutionAdded(address indexed institution);
    event InstitutionRemoved(address indexed institution);

    // --- State Variables ---

    // Represents the status of a certificate.
    enum Status { Unissued, Issued, Revoked }

    // Struct to hold certificate details.
    struct CertificateDetails {
        Status status;
        address issuingInstitution;
        uint256 timestamp;
    }

    // Mapping from certificate hash to its details.
    mapping(bytes32 => CertificateDetails) private _certificates;

    // A set of addresses for authorized educational institutions.
    EnumerableSet.AddressSet private _institutions;

    // --- Modifiers ---

    /**
     * @dev Throws if called by any account that is not an authorized institution.
     */
    modifier onlyInstitution() {
        require(_institutions.contains(msg.sender), "Caller is not an authorized institution");
        _;
    }

    // --- Constructor ---

    constructor(address initialOwner) Ownable(initialOwner) {}

    // --- Institution Management Functions (Owner only) ---

    /**
     * @dev Adds a new institution to the set of authorized issuers.
     * @param institutionAddress The address of the institution to add.
     */
    function addInstitution(address institutionAddress) external onlyOwner {
        require(institutionAddress != address(0), "Invalid address");
        require(_institutions.add(institutionAddress), "Institution already exists");
        emit InstitutionAdded(institutionAddress);
    }

    /**
     * @dev Removes an institution from the set of authorized issuers.
     * @param institutionAddress The address of the institution to remove.
     */
    function removeInstitution(address institutionAddress) external onlyOwner {
        require(_institutions.remove(institutionAddress), "Institution does not exist");
        emit InstitutionRemoved(institutionAddress);
    }

    // --- Certificate Lifecycle Functions (Institution only) ---

    /**
     * @dev Issues a new certificate by storing its hash.
     * @param certificateHash The keccak256 hash of the off-chain certificate data.
     */
    function issueCertificate(bytes32 certificateHash) external onlyInstitution {
        require(_certificates[certificateHash].status == Status.Unissued, "Certificate already exists");

        _certificates[certificateHash] = CertificateDetails({
            status: Status.Issued,
            issuingInstitution: msg.sender,
            timestamp: block.timestamp
        });

        emit CertificateIssued(certificateHash, msg.sender, block.timestamp);
    }

    /**
     * @dev Revokes an existing certificate.
     * @param certificateHash The hash of the certificate to revoke.
     */
    function revokeCertificate(bytes32 certificateHash) external onlyInstitution {
        CertificateDetails storage cert = _certificates[certificateHash];
        require(cert.status == Status.Issued, "Certificate not in issued state");
        // Optional: require(cert.issuingInstitution == msg.sender, "Only the issuing institution can revoke");

        cert.status = Status.Revoked;
        emit CertificateRevoked(certificateHash, msg.sender, block.timestamp);
    }

    // --- Public View Functions ---

    /**
     * @dev Verifies the status of a certificate.
     * @param certificateHash The hash of the certificate to verify.
     * @return The status, issuing institution, and timestamp of the certificate.
     */
    function getCertificateStatus(bytes32 certificateHash) external view returns (Status, address, uint256) {
        CertificateDetails storage cert = _certificates[certificateHash];
        return (cert.status, cert.issuingInstitution, cert.timestamp);
    }

    /**
     * @dev Checks if an address is an authorized institution.
     * @param institutionAddress The address to check.
     * @return True if the address is an institution, false otherwise.
     */
    function isInstitution(address institutionAddress) external view returns (bool) {
        return _institutions.contains(institutionAddress);
    }

    /**
     * @dev Returns the number of authorized institutions.
     */
    function getInstitutionCount() external view returns (uint256) {
        return _institutions.length();
    }

    /**
     * @dev Returns an institution at a specific index.
     */
    function getInstitutionAtIndex(uint256 index) external view returns (address) {
        return _institutions.at(index);
    }
}
