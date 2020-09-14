from brownie import *
from config import *

c = MainnetConfig()

def main():
    assert c.STEAK_TOKEN == "", 'STEAK is already deployed'

    deployer_acc = accounts.load(c.DEPLOYER)
    steak = SteakToken.deploy({"from": deployer_acc})

    print('Set in config.py:')
    print(f'    STEAK_TOKEN = "{steak.address}"')
