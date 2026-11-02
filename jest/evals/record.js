// evals/record.js: a test calls record({ output }) before its expect
const fs = require("node:fs")
const FILE = "reports/eval-properties.jsonl"
exports.FILE = FILE
exports.record = (props) => {
  fs.mkdirSync("reports", { recursive: true })
  fs.appendFileSync(FILE, JSON.stringify({ test: expect.getState().currentTestName, ...props }) + "\n")
}
