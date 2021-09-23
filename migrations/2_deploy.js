// migrations/2_deploy.js
// SPDX-License-Identifier: MIT
const Serial = artifacts.require("Serial");
module.exports = function(deployer) {
  deployer.deploy(Serial, "The Serials", "SER", "ipfs://QmQhoe435ssjAdkDx3nLNV1MencWjuneFaqrAGBHsYWfou/")
}
