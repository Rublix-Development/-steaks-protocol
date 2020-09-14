from brownie import *
from config import *

c = MainnetConfig()

def main():
    assert c.STEAK_TOKEN, 'STEAK Token not set'
    assert c.TIMELOCK == "", 'Timelock is already deployed'
    assert c.GOVERNOR == "", 'Governor is already deployed'
    deployer_acc = accounts.load(c.DEPLOYER)

    gov_delay = 2 * 24 * 3600  # 2 days
    # TODO: figure out the admin initialization thing
    admin_acc = deployer_acc.address
    timelock = Timelock.deploy(admin_acc, gov_delay, {"from": deployer_acc})

    guardian = deployer_acc.address
    gov = GovernorAlpha.deploy(timelock.address, c.STEAK_TOKEN, guardian, {"from": deployer_acc})

    print('Set in config.py:')
    print(f'    TIMELOCK = "{timelock.address}"')
    print(f'    GOVERNOR = "{gov.address}"')
