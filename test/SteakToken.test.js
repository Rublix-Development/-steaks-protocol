const { expectRevert } = require('@openzeppelin/test-helpers');
const SteakToken = artifacts.require('SteakToken');

contract('SteakToken', ([alice, bob, carol]) => {
    beforeEach(async () => {
        this.steak = await SteakToken.new({ from: alice });
    });

    it('should have correct name and symbol and decimal', async () => {
        const name = await this.steak.name();
        const symbol = await this.steak.symbol();
        const decimals = await this.steak.decimals();
        assert.equal(name.valueOf(), 'Steaks.finance');
        assert.equal(symbol.valueOf(), 'STEAK');
        assert.equal(decimals.valueOf(), '18');
    });

    it('should only allow owner to mint token', async () => {
        await this.steak.mint(alice, '100', { from: alice });
        await this.steak.mint(bob, '1000', { from: alice });
        await expectRevert(
            this.steak.mint(carol, '1000', { from: bob }),
            'Ownable: caller is not the owner',
        );
        const totalSupply = await this.steak.totalSupply();
        const aliceBal = await this.steak.balanceOf(alice);
        const bobBal = await this.steak.balanceOf(bob);
        const carolBal = await this.steak.balanceOf(carol);
        assert.equal(totalSupply.valueOf(), '1100');
        assert.equal(aliceBal.valueOf(), '100');
        assert.equal(bobBal.valueOf(), '1000');
        assert.equal(carolBal.valueOf(), '0');
    });

    it('should supply token transfers properly', async () => {
        await this.steak.mint(alice, '100', { from: alice });
        await this.steak.mint(bob, '1000', { from: alice });
        await this.steak.transfer(carol, '10', { from: alice });
        await this.steak.transfer(carol, '100', { from: bob });
        const totalSupply = await this.steak.totalSupply();
        const aliceBal = await this.steak.balanceOf(alice);
        const bobBal = await this.steak.balanceOf(bob);
        const carolBal = await this.steak.balanceOf(carol);
        assert.equal(totalSupply.valueOf(), '1100');
        assert.equal(aliceBal.valueOf(), '90');
        assert.equal(bobBal.valueOf(), '900');
        assert.equal(carolBal.valueOf(), '110');
    });

    it('should fail if you try to do bad transfers', async () => {
        await this.steak.mint(alice, '100', { from: alice });
        await expectRevert(
            this.steak.transfer(carol, '110', { from: alice }),
            'ERC20: transfer amount exceeds balance',
        );
        await expectRevert(
            this.steak.transfer(carol, '1', { from: bob }),
            'ERC20: transfer amount exceeds balance',
        );
    });
  });
