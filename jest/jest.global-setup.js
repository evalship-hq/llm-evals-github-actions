// jest.global-setup.js, set as globalSetup in package.json: clears the last run's properties
module.exports = () => require("node:fs").rmSync(require("./evals/record").FILE, { force: true })
