from brownie import *
from config import *
import time

c = MainnetConfig()

deployer_acc = accounts.load(c.DEPLOYER)
factory = UniswapV2Factory.at(c.V2_FACTORY)
maker = SteakMaker.at(c.STEAK_MAKER)

def convert_lp(tokenA, tokenB):
    """Convert Poolshares into STEAK, send them to Bar"""
    maker.convert(tokenA, tokenB, {"from": deployer_acc})


def main():
    convert_lp(
        c.WETH,
        "0xF1290473E210b2108A85237fbCd7b6eb42Cc654F"
    )
