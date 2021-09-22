// migrations/2_deploy.js
// SPDX-License-Identifier: MIT
const Serial = artifacts.require("Serial");
module.exports = function(deployer) {
  deployer.deploy(Serial, "The Serials", "SER", "ipfs://QmVwccJeRcKi8Rv6hAjcEBUVJuNideRS8MrKexGQfmj2de/")
}
