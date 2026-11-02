// junitTestCaseProperties.js, next to package.json: jest-junit calls it once per test
const fs = require("node:fs")
const { FILE } = require("./evals/record")
const byTest = new Map(
  (fs.existsSync(FILE) ? fs.readFileSync(FILE, "utf8").trim().split("\n") : [])
    .filter(Boolean).map((line) => JSON.parse(line)).map(({ test, ...props }) => [test, props]),
)
module.exports = (testResult) => byTest.get(testResult.fullName) ?? {}
