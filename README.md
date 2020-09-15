

## Steaks.finance  ![](steak-logo.png)

## Deployed Contracts / Hash

- Steaks Token - <https://etherscan.io/token/0x6b3595068778dd592e39a122f4f5a5cf09c90fe2>
- MasterChef - <https://etherscan.io/address/0xc2edad668740f1aa35e4d8f227fb8e17dca888cd>
- (Uni|Steak)swapV2Factory - <https://etherscan.io/address/0xc0aee478e3658e2610c5f7a4a2e1777ce9e4f2ac>
- (Uni|Steak)swapV2Router02 - <https://etherscan.io/address/0xd9e1ce17f2641f24ae83637ab66a2cca9c378b9f>
- (Uni|Steak)swapV2Pair init code hash - `e18a34eb0e04b04f7a0ac29a6e80748dca96319b42c54d679cb821dca90c6303`
- SteakBar - <https://etherscan.io/address/0x8798249c2e607446efb7ad49ec89dd1865ff4272>
- SteakMaker - <https://etherscan.io/address/0x54844afe358ca98e4d09aae869f25bfe072e1b1a>



### STEAKS Token Flow

![](token-flow.png)



## Set up local environment

### Dependencies

Install `ganache` and `truffle` clis:

```
npm install -g ganache-cli truffle truffle-flattener
npm i
```

You need python dev package, the below command works for Ubuntu:

```
sudo apt install libpython3.8-dev
```

Install `pipenv` environment:

```
pipenv sync
```

Install [Metamask](https://metamask.io/download.html).



## Deployment
First we need to import the Deployer account (will be prompted to enter private key):
```
pipenv run brownie accounts new deployer
```

If not already, set `WEB3_INFURA_PROJECT_ID` in `.env`.

### Deploy the STEAK token

```
pipenv run brownie run deploy/0_steak_token.py --network mainnet
```

Set the `STEAK_TOKEN` address  in `config.py`.

### Deploy the DAO

```
pipenv run brownie run deploy/1_governance.py --network mainnet
```

Set the `TIMELOCK`  and `GOVERNOR` addresses  in `config.py`.

### Deploy the SteakSwap exchange

```
pipenv run brownie run deploy/2_steakswap.py --network mainnet
```

Set the `V2_FACTORY`  and `V2_ROUTER` addresses  in `config.py`.

### Deploy the MasterChef 

```
pipenv run brownie run deploy/3_masterchef.py --network mainnet
```

Set the `STEAK_BAR`, `STEAK_MAKER`, `MASTER_CHEF` and `MIGRATOR` addresses  in `config.py`.

## Generate the Etherscan Contract Verification codes

For each deployed contract, a `truffle-flattener` must run, ie:

```
truffle-flattener contracts/SteakToken.sol > etherscan.sol
```
The code of the flattener output needs to be modified to:
 - match solc version used by Brownie on all contracts
 - remove duplicate SPDX-License identifiers
