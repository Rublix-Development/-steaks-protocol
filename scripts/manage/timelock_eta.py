from brownie import *
from config import *

c = MainnetConfig()

def main():
    delay = 50 * 3600
    eta = web3.eth.getBlock('latest')['timestamp'] + delay
    print(eta)
