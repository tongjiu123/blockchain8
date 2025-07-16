// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title CertificateOnChain
 * @dev A baseline contract for comparison, storing all certificate data directly on-chain.
 * This contract is intentionally designed to be less efficient to highlight the benefits
 * of the hybrid storage model in the main `Certificate` contract.
 */
contract CertificateOnChain is Ownable {

    // --- Events ---
    event CertificateIssued(uint256 indexed certificateId, address indexed institution, string studentName);

    // --- State Variables ---

    struct CertificateData {
        string studentName;
        string degreeType;
        string institutionName;
        uint256 issueTimestamp;
        address issuingInstitution;
        bool isIssued;
    }

    // Using an array to store certificate data to simulate a simple on-chain list.
    CertificateData[] public certificates;

    // Mapping from an ID to its index in the array for quick lookup, though not used in this simple version.
    mapping(uint256 => uint256) private certificateIndex;

    // --- Constructor ---

    constructor(address initialOwner) Ownable(initialOwner) {}

    // --- Certificate Issuance Function ---

    /**
     * @dev Issues a new certificate by storing all its data on-chain.
     * This function will consume a significant amount of gas, especially with longer strings.
     * @param studentName The name of the student.
     * @param degreeType The type of degree awarded.
     * @param institutionName The name of the issuing institution.
     */
    function issueCertificate(
        string calldata studentName,
        string calldata degreeType,
        string calldata institutionName
    ) external onlyOwner {
        uint256 certificateId = certificates.length;

        certificates.push(CertificateData({
            studentName: studentName,
            degreeType: degreeType,
            institutionName: institutionName,
            issueTimestamp: block.timestamp,
            issuingInstitution: msg.sender,
            isIssued: true
        }));

        certificateIndex[certificateId] = certificateId; // Simple index mapping

        emit CertificateIssued(certificateId, msg.sender, studentName);
    }

    // --- Public View Functions ---

    /**
     * @dev Retrieves the full data of a certificate.
     * @param certificateId The ID of the certificate to retrieve.
     * @return The full certificate data.
     */
    function getCertificateData(uint256 certificateId) external view returns (CertificateData memory) {
        require(certificateId < certificates.length, "Certificate ID out of bounds");
        return certificates[certificateId];
    }

    /**
     * @dev Returns the total number of certificates issued.
     */
    function getCertificateCount() external view returns (uint256) {
        return certificates.length;
    }
}
