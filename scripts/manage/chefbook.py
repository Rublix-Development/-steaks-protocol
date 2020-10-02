from brownie import *
from config import *
import time

from eth_abi import encode_abi

c = MainnetConfig()

deployer_acc = accounts.load(c.DEPLOYER)
factory = UniswapV2Factory.at(c.V2_FACTORY)
chef = MasterChef.at(c.MASTER_CHEF)
timelock = Timelock.at(c.TIMELOCK)

# pid:[lp_addr, alloc_point]
uniswap_pools_1 = {
    0: ["0xDA73Ce7778C87131B6aD4210999De8d93B0a28e9", 400],  # HEDG-ETH
    1: ["0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc", 50],   # USDC-ETH
    2: ["0x004375Dff511095CC5A197A54140a24eFEF3A416", 50],   # USDC-WBTC
    3: ["0xa2107FA5B38d9bbd2C461D6EDf11B11A50F6b974", 200],  # LINK-ETH
    4: ["0xd3d2E2692501A5c9Ca623199D38826e513033a17", 200],  # UNI-ETH
    5: ["0xCFfDdeD873554F362Ac02f8Fb1f02E5ada10516f", 200],  # COMP-ETH
    6: ["0x2fDbAdf3C4D5A8666Bc06645B8358ab803996E28", 200],  # YFI-ETH
}
uniswap_pools_2 = {
    7: ["0xBb2b8038a1640196FbE3e38816F3e67Cba72D940", 50],   # WBTC-ETH
}
uniswap_pools_3 = {
    8: ["0x99b46782E350A37D2850fF3713bF29Ab3902CD31", 800],  # STEAK-ETH
}
uniswap_pools_4 = {
    9:  ["0x48e130B740Af7D2bAc0Ee7E0dF95dcdC3F6eA162", 100],  # USDC-STEAK
    10: ["0x82e51A70E199F5a25E56Ea55f4229DcdDB822AFD", 100],  # WBTC-STEAK
}
uniswap_pools_5 = {
    11: ["0x43AE24960e5534731Fc831386c07755A2dc33D47", 5],  # SNX-ETH
}
uniswap_pools_6 = {
    12: ["0xFc2890ffB3069A1A9d3F7B11C7775a1A1ee721c0", 0],  # USDC-HEDG
}
uniswap_pools_7 = {
    13: ["0xF5cAFa398bEB12dCCFBA917c19922C1EA2d6c056", 0],  # HEDG-STEAK
}
uniswap_pools_8 = {
    14: ["0xdc98556Ce24f007A5eF6dC1CE96322d65832A819", 0],  # PICKLE-ETH
    15: ["0xCE84867c3c02B05dc570d0135103d3fB9CC19433", 0],  # SUSHI-ETH
    16: ["0xAE461cA67B15dc8dc81CE7615e0320dA1A9aB8D5", 0],  # DAI-USDC
}
pools_update_to = {
    0:  ["0xDA73Ce7778C87131B6aD4210999De8d93B0a28e9",   60],  # HEDG-ETH
    1:  ["0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",   25],  # USDC-ETH
    2:  ["0x004375Dff511095CC5A197A54140a24eFEF3A416",    0],  # USDC-WBTC
    3:  ["0xa2107FA5B38d9bbd2C461D6EDf11B11A50F6b974",   15],  # LINK-ETH
    4:  ["0xd3d2E2692501A5c9Ca623199D38826e513033a17",   15],  # UNI-ETH
    5:  ["0xCFfDdeD873554F362Ac02f8Fb1f02E5ada10516f",   15],  # COMP-ETH
    6:  ["0x2fDbAdf3C4D5A8666Bc06645B8358ab803996E28",   25],  # YFI-ETH
    7:  ["0xBb2b8038a1640196FbE3e38816F3e67Cba72D940",   25],  # WBTC-ETH
    8:  ["0x99b46782E350A37D2850fF3713bF29Ab3902CD31",  200],  # STEAK-ETH
    9:  ["0x48e130B740Af7D2bAc0Ee7E0dF95dcdC3F6eA162",    0],  # USDC-STEAK
    10: ["0x82e51A70E199F5a25E56Ea55f4229DcdDB822AFD",    0],  # WBTC-STEAK
    11: ["0x43AE24960e5534731Fc831386c07755A2dc33D47",   15],  # SNX-ETH
    12: ["0xFc2890ffB3069A1A9d3F7B11C7775a1A1ee721c0",   50],  # USDC-HEDG
    13: ["0xF5cAFa398bEB12dCCFBA917c19922C1EA2d6c056",    0],  # HEDG-STEAK
    14: ["0xdc98556Ce24f007A5eF6dC1CE96322d65832A819",   20],  # PICKLE-ETH
    15: ["0xCE84867c3c02B05dc570d0135103d3fB9CC19433",   25],  # SUSHI-ETH
    16: ["0xAE461cA67B15dc8dc81CE7615e0320dA1A9aB8D5",   10],  # DAI-USDC
}


def prevent_double_add(lp_addr: str):
    for i in range(100):
        try:
            pool = chef.poolInfo(i)
        except ValueError:
            break
        assert pool[0] != lp_addr, 'Pool already exists'

def initialize_pools(pools: dict):
    """Setup initial UniswapV2-LP farms"""
    for lp_addr, alloc_point in list(pools.values()):
        prevent_double_add(lp_addr)
        chef.add(alloc_point, lp_addr, False, {"from": deployer_acc,
                                               "gas_price": int(web3.eth.gasPrice*1.3)})
    time.sleep(30)
    chef.massUpdatePools({"from": deployer_acc})

def update_pools(pools: dict):
    for pid, (lp_addr, alloc_point) in pools.items():
        print(f"Changing pool {pid} ({lp_addr}) to {alloc_point}")
        change_pool_alloc(pid, lp_addr, alloc_point, False)

    time.sleep(30)
    chef.massUpdatePools({"from": deployer_acc})

def add_pool(lp_addr: str, alloc_point: int, refresh=True):
    """Manually add a pool (ie. Uniswap ETH-STEAKS)"""
    prevent_double_add(lp_addr)
    chef.add(alloc_point, lp_addr, refresh, {"from": deployer_acc})

def change_pool_alloc(pid: int, lp_addr: str, alloc_point: int, refresh=True):
    """Change pool rewards allocation"""
    assert chef.poolInfo(pid)[0] == lp_addr, 'Wrong pool id/addr'
    chef.set(pid, alloc_point, refresh, {"from": deployer_acc,
                                         "gas_price": int(web3.eth.gasPrice*1.3)})

def migrate_pools(pools: dict):
    """Migrate liquidity from Uniswap to SteakSwap"""
    for pid in list(pools.keys()):
        chef.migrate(pid, {"from": deployer_acc,
                           "gas_price": int(web3.eth.gasPrice*1.3)})
    disable_migrator()

def set_migrator(migrator_contract_addr: str):
    """Call this after deploying new Migrator (usually not needed)"""
    factory.setMigrator(migrator_contract_addr, {"from": deployer_acc})
    chef.setMigrator(migrator_contract_addr, {"from": deployer_acc})
    assert factory.migrator() == migrator_contract_addr, 'Invalid migrator'
    assert chef.migrator() == migrator_contract_addr, 'Invalid migrator'

def disable_migrator():
    """Call this AFTER migration from Uniswap to SteakSwap"""
    factory.setMigrator(c.NULL_ADDRESS, {"from": deployer_acc})
    chef.setMigrator(c.NULL_ADDRESS, {"from": deployer_acc})
    assert factory.migrator() == c.NULL_ADDRESS, 'Invalid migrator'
    assert chef.migrator() == c.NULL_ADDRESS, 'Invalid migrator'

def update_pool(pid: int):
    """Call this to manually update revenue numbers.
    Typically necessary in production."""
    chef.updatePool(pid, {"from": deployer_acc})


def enable_timelock():
    chef.transferOwnership(c.TIMELOCK, {"from": deployer_acc,
                                        "gas_price": int(web3.eth.gasPrice*1.3)})


def initialize_pools_timelock(pools: dict, action: str, eta: int):
    for lp_addr, alloc_point in list(pools.values()):
        prevent_double_add(lp_addr)
        exec_timelock(
            action,
            chef.address,
            "add(uint256,address,bool)",
            encode_abi(['uint256', 'address', 'bool'], [alloc_point, lp_addr, True]),
            eta,
        )


def update_pools_timelock(pools: dict, action: str, eta: int):
    for pid, (lp_addr, alloc_point) in pools.items():
        assert chef.poolInfo(pid)[0] == lp_addr, 'Wrong pool id/addr'
        print(f"Changing pool {pid} ({lp_addr}) to {alloc_point}")
        exec_timelock(
            action,
            chef.address,
            "set(uint256,unit256,bool)",
            encode_abi(['uint256', 'uint256', 'bool'], [pid, alloc_point, True]),
            eta,
        )


def exec_timelock(action: str, address: str, signature: str, abi: bytes, eta: int):
        if action == 'queue':
            timelock_fn = timelock.queueTransaction
        if action == 'execute':
            timelock_fn = timelock.executeTransaction
        if action == 'cancel':
            timelock_fn = timelock.cancelTransaction

        timelock_fn(
            address,
            0, # send no eth
            signature,
            abi,
            eta,
            {'from': deployer_acc, "gas_price": int(web3.eth.gasPrice*1.3)},
        )



def main():
    # initialize_pools(uniswap_pools_1) # done
    # initialize_pools(uniswap_pools_2) # done
    # initialize_pools(uniswap_pools_3) # done
    # initialize_pools(uniswap_pools_4) # done
    # initialize_pools(uniswap_pools_5) # done
    # initialize_pools(uniswap_pools_6) # done
    # initialize_pools(uniswap_pools_7) # done
    # update_pools(pools_update_to)     # done
    # enable_timelock()                 # done

    # generated with timelock_eta.py
    eta = 1601828870
    action = 'queue' # queue, execute or cancel
    initialize_pools_timelock(uniswap_pools_8, action, eta)
    update_pools_timelock(pools_update_to, action, eta)

    # migrate_pools(uniswap_pools)
    # disable_migrator()
    pass
