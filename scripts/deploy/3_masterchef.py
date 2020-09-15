from brownie import *
from config import *

c = MainnetConfig()

def main():
    assert c.WETH, 'WETH Contract not set'
    assert c.STEAK_TOKEN, 'STEAK Token not set'
    assert c.V2_FACTORY, 'Factory not set'
    assert c.UNISWAP_FACTORY, 'Uniswap Factory not set'
    assert c.STEAK_BAR == "", 'SteakBar is already deployed'
    assert c.STEAK_MAKER == "", 'SteakMaker is already deployed'
    assert c.MASTER_CHEF == "", 'MasterChef is already deployed'
    assert c.MIGRATOR == "", 'Migrator is already deployed'

    deployer_acc = accounts.load(c.DEPLOYER)

    factory = UniswapV2Factory.at(c.V2_FACTORY)

    steak = SteakToken.at(c.STEAK_TOKEN)
    steak_bar = SteakBar.deploy(steak.address, {"from": deployer_acc})
    steak_maker = SteakMaker.deploy(
        c.V2_FACTORY,
        steak.address,
        steak_bar.address,
        c.WETH,
        {"from": deployer_acc})

    # make SteakMaker earn trading fees
    factory.setFeeTo(steak_maker.address, {"from": deployer_acc})
    assert factory.feeTo() == steak_maker.address, 'Maker has receive fees'

    # developer fund fee recipient
    devaddr = deployer_acc.address
    start_block = 0
    steak_per_block = 0
    bonus_end_block = 0
    master_chef = MasterChef.deploy(
        steak.address,
        devaddr,
        steak_per_block,
        start_block,
        bonus_end_block,
        {"from": deployer_acc})

    migration_start_block = 0
    migrator = Migrator.deploy(
        master_chef.address,
        c.UNISWAP_FACTORY,
        c.V2_FACTORY,
        migration_start_block,
        {"from": deployer_acc})

    # link the migrator contract
    master_chef.setMigrator(migrator.address)
    assert master_chef.migrator() == migrator.address, 'Invalid migrator'

    factory.setMigrator(migrator.address)
    assert factory.migrator() == migrator.address, 'Invalid migrator'


    print('Set in config.py:')
    print(f'    STEAK_BAR = "{steak_bar.address}"')
    print(f'    STEAK_MAKER = "{steak_maker.address}"')
    print(f'    MASTER_CHEF = "{master_chef.address}"')
    print(f'    MIGRATOR = "{migrator.address}"')