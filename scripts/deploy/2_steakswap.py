from brownie import *
from config import *

c = MainnetConfig()

def main():
    assert c.WETH, 'WETH Contract not set'
    assert c.V2_PAIR_HASH, 'Pair hash not set'
    assert c.V2_FACTORY == "", 'Factory is already deployed'
    assert c.V2_ROUTER == "", 'Router is already deployed'
    deployer_acc = accounts.load(c.DEPLOYER)

    fee_setter = deployer_acc.address
    factory = UniswapV2Factory.deploy(fee_setter, {"from": deployer_acc})
    assert str(factory.pairCodeHash())[2:] == c.V2_PAIR_HASH, 'Pair hash mismatch'
    router = UniswapV2Router02.deploy(factory.address, c.WETH, {"from": deployer_acc})

    print('Set in config.py:')
    print(f'    V2_PAIR_HASH = "{factory.pairCodeHash()}"')
    print(f'    V2_FACTORY   = "{factory.address}"')
    print(f'    V2_ROUTER    = "{router.address}"')

