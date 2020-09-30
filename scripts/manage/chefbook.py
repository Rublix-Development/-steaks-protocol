from brownie import *
from config import *
import time

c = MainnetConfig()

deployer_acc = accounts.load(c.DEPLOYER)
factory = UniswapV2Factory.at(c.V2_FACTORY)
chef = MasterChef.at(c.MASTER_CHEF)

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
pools_update_to = {
    0:  ["0xDA73Ce7778C87131B6aD4210999De8d93B0a28e9",  100],  # HEDG-ETH
    1:  ["0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc",    2],  # USDC-ETH
    2:  ["0x004375Dff511095CC5A197A54140a24eFEF3A416",    0],  # USDC-WBTC
    3:  ["0xa2107FA5B38d9bbd2C461D6EDf11B11A50F6b974",    5],  # LINK-ETH
    4:  ["0xd3d2E2692501A5c9Ca623199D38826e513033a17",    5],  # UNI-ETH
    5:  ["0xCFfDdeD873554F362Ac02f8Fb1f02E5ada10516f",    5],  # COMP-ETH
    6:  ["0x2fDbAdf3C4D5A8666Bc06645B8358ab803996E28",    5],  # YFI-ETH
    7:  ["0xBb2b8038a1640196FbE3e38816F3e67Cba72D940",    2],  # WBTC-ETH
    8:  ["0x99b46782E350A37D2850fF3713bF29Ab3902CD31",  100],  # STEAK-ETH
    9:  ["0x48e130B740Af7D2bAc0Ee7E0dF95dcdC3F6eA162",  100],  # USDC-STEAK
    10: ["0x82e51A70E199F5a25E56Ea55f4229DcdDB822AFD",  100],  # WBTC-STEAK
    11: ["0x43AE24960e5534731Fc831386c07755A2dc33D47",    5],  # SNX-ETH
    12: ["0xFc2890ffB3069A1A9d3F7B11C7775a1A1ee721c0",    0],  # USDC-HEDG
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

def main():
    # initialize_pools(uniswap_pools_1) # done
    # initialize_pools(uniswap_pools_2) # done
    # initialize_pools(uniswap_pools_3) # done
    # initialize_pools(uniswap_pools_4) # done
    # initialize_pools(uniswap_pools_5) # done
    # initialize_pools(uniswap_pools_6) # done
    update_pools(pools_update_to)

    # migrate_pools(uniswap_pools)
    # disable_migrator()
    pass
