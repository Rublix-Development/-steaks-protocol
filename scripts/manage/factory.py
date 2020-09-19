from brownie import *
from config import *

c = MainnetConfig()

def main():
    assert c.V2_FACTORY, 'Factory not set'
    factory = UniswapV2Factory.at(c.V2_FACTORY)
    print('Address:', factory.address)
    print('Codehash:', factory.pairCodeHash())
