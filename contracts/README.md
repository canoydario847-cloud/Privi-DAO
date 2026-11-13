# Base governance contracts (source only)

- `PriviDAOToken.sol`: separate Base ERC20Votes token **PDAO**, fixed 1,000,000,000 supply, all initially assigned to a chosen deployment recipient. This is NOT the native chain PRVI coin nor the BNB PRIV token. Token allocations and the recipient need explicit approval before deployment.
- `PriviGovernor.sol`: OpenZeppelin Governor + token snapshots, 4% quorum, standard block-clock voting delay and voting period. **Settings are provisional**; Base has faster blocks than Ethereum, so tune delays using actual on-chain time before deployment.
- `PriviServiceRegistry.sol`: permissioned governance metadata registry; service registration does **not** grant control of external systems or certify them as operational.
- A TimelockController is deployed separately. Set proposers/executors only after careful configuration, revoke unnecessary admin roles, and put a multisig in the emergency/admin design. Timelock ownership should not be transferred before review.
- No token, governor, registry, treasury, pool, or liquidity has been deployed by this repository change. Do not advertise a live PDAO address.
- Use OpenZeppelin Contracts **5.x** and Solidity **0.8.24+**, pin dependency versions and run compilation, unit tests, security review and Base Sepolia rehearsal before considering Base mainnet.
- The off-chain `services/catalog.json` lists known Privi repos and described projects, including unverified ones. Actual DAO control requires explicit ownership grants, contract permissions, or approved API integrations; inventory alone does not authorize changes.
- AI agent has recommendation/monitoring scope only. No keys or autonomous treasury spending.
