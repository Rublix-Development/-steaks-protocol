from brownie import *
from config import *

c = MainnetConfig()

deployer_acc = accounts.load(c.DEPLOYER)
factory = UniswapV2Factory.at(c.V2_FACTORY)
chef = MasterChef.at(c.MASTER_CHEF)

# pid:[lp_addr, alloc_point]
uniswap_pools = {
    0: ["0xDA73Ce7778C87131B6aD4210999De8d93B0a28e9", 100],  # ETH-HEDG
    1: ["0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852", 10],  # ETH-USDT
    2: ["0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc", 10],  # ETH-USDC
    3: ["0x3041CbD36888bECc7bbCBc0045E3B1f144466f5f", 10],  # USDC-USDT
    4: ["0xCE84867c3c02B05dc570d0135103d3fB9CC19433", 10],  # ETH-SUSHI
    5: ["0x2fDbAdf3C4D5A8666Bc06645B8358ab803996E28", 10],  # ETH-YFI
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

def main():
    pass
