const AsymPool = artifacts.require("AsymPool");

module.exports = (deployer) => {
    deployer.deploy(AsymPool)
}