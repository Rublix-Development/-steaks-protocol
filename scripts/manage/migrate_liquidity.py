from brownie import *
from config import *

c = MainnetConfig()

deployer_acc = accounts.load(c.DEPLOYER)
factory = UniswapV2Factory.at(c.V2_FACTORY)
chef = MasterChef.at(c.MASTER_CHEF)

# pid:[lp_addr, alloc_point]
uniswap_pools = {
    0: ["0xda73ce7778c87131b6ad4210999de8d93b0a28e9", 10],  # ETH-HEDG
    1: ["0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852", 10],  # ETH-USDT
}


def initialize_pools():
    """Setup initial UniswapV2-LP farms"""
    assert chef.poolLength() == 0, 'Pools already initialized'
    for lp_addr, alloc_point in list(uniswap_pools.values()):
        chef.add(alloc_point, lp_addr, False, {"from": deployer_acc})
    chef.massUpdatePools({"from": deployer_acc})

def add_pool(lp_addr: str, alloc_point: int):
    """Manually add a pool (ie. Uniswap ETH-STEAKS)"""
    assert not any([x.lpToken() == lp_addr for x in chef.poolInfo()]), 'Already exists'
    chef.add(alloc_point, lp_addr, False, {"from": deployer_acc})
    chef.massUpdatePools({"from": deployer_acc})

def migrate_pools():
    """Migrate liquidity from Uniswap to SteakSwap"""
    for pid in list(uniswap_pools.keys()):
        chef.migrate(pid, {"from": deployer_acc})

def disable_migrator():
    """Call this AFTER migration from Uniswap to SteakSwap"""
    factory.setMigrator(c.NULL_ADDRESS, {"from": deployer_acc})
    chef.setMigrator(c.NULL_ADDRESS, {"from": deployer_acc})
    assert factory.migrator() == c.NULL_ADDRESS, 'Invalid migrator'
    assert chef.migrator() == c.NULL_ADDRESS, 'Invalid migrator'

def main():
    pass
