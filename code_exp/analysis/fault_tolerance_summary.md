# Fault Tolerance Test Results

## Overview
This experiment evaluated the system's resilience to node failures in a multi-node blockchain network. We tested three scenarios with varying numbers of failed nodes and measured availability, recovery time, and data consistency.

## Test Scenarios
| Scenario | Active Nodes | Failed Nodes | Fault Duration (s) |
|----------|-------------|-------------|-------------------|
| Normal Operation | 4 | 0 | 30 |
| Single Node Failure | 3 | 1 | 30 |
| Double Node Failure | 2 | 2 | 30 |
| Extreme Failure | 1 | 3 | 30 |

## Availability Results
| Scenario | Availability | Successful Txs | Failed Txs |
|----------|-------------|---------------|------------|
| Normal Operation | 0.86 | 43 | 7 |
| Single Node Failure | 1.00 | 50 | 0 |
| Double Node Failure | 1.00 | 50 | 0 |
| Extreme Failure | 1.00 | 50 | 0 |

## Recovery Results
| Scenario | Recovery Time (s) | Sync Complete | Data Consistent |
|----------|------------------|---------------|----------------|
| Normal Operation | 70.38 | False | True |
| Single Node Failure | 73.59 | False | True |
| Double Node Failure | 76.79 | False | False |
| Extreme Failure | 79.86 | False | False |

## Key Findings
- **Average System Availability**: 0.96 (or 96.5%)
- **Average Recovery Time**: 75.16 seconds
- **Best Availability Scenario**: Single Node Failure
- **Fastest Recovery Scenario**: Normal Operation
- **Data Consistency**: Maintained in Normal Operation, Single Node Failure

## Visualization
![Fault Tolerance Test Results](./fig6_fault_tolerance.png)

## Conclusion
The fault tolerance test demonstrates that our blockchain-based academic credential system maintains good availability even when multiple nodes fail. Data consistency is maintained in scenarios with limited node failures, and recovery times increase with the number of failed nodes. These results highlight the trade-offs between availability, consistency, and recovery time in distributed blockchain systems and provide insights for optimizing fault tolerance mechanisms.