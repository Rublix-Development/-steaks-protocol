from brownie import *
from config import *

c = MainnetConfig()

deployer_acc = accounts.load(c.DEPLOYER)
