from brownie import *
from config import *

c = MainnetConfig()



def deploy_factory():
    assert c.V2_FACTORY == "", 'Factory is already deployed'
    deployer_acc = accounts.load(c.DEPLOYER)

    fee_setter = deployer_acc.address
    factory = UniswapV2Factory.deploy(fee_setter, {"from": deployer_acc})

    print('Set in config.py:')
    print(f'    V2_FACTORY   = "{factory.address}"')
    print(f'    V2_PAIR_HASH = "{factory.pairCodeHash()}"')

def deploy_router():
    assert c.WETH, 'WETH Contract not set'
    assert c.V2_FACTORY == "", 'Factory is already deployed'
    assert c.V2_ROUTER == "", 'Router is already deployed'
    deployer_acc = accounts.load(c.DEPLOYER)

    fee_setter = deployer_acc.address
    factory = UniswapV2Factory.deploy(fee_setter, {"from": deployer_acc})
    router = UniswapV2Router02.deploy(factory.address, c.WETH, {"from": deployer_acc})

    print('Set in config.py:')
    print(f'    V2_ROUTER    = "{router.address}"')

def main():
    deploy_factory()

