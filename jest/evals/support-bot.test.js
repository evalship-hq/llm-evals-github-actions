const { classify } = require("../support-bot")
const { record } = require("./record")

const cases = [
  { id: "double-charge", message: "I was charged twice for my subscription this month.", expected: "billing" },
  { id: "refund-request", message: "Can I get a refund for the annual plan I bought yesterday?", expected: "billing" },
  { id: "app-crash", message: "The app crashes every time I open the settings page.", expected: "bug" },
  { id: "export-error", message: "Exporting a report to CSV fails with a 500 error.", expected: "bug" },
  { id: "dark-mode", message: "Could you add a dark mode?", expected: "other" },
  { id: "support-hours", message: "What are your support hours?", expected: "other" },
]

const hasKey = Boolean(process.env.ANTHROPIC_API_KEY)
if (!hasKey) console.warn("ANTHROPIC_API_KEY is not set, so the evals can't call the model. Skipping them.")

describe("support bot", () => {
  ;(hasKey ? test : test.skip).each(cases)("$id", async ({ message, expected }) => {
    const label = await classify(message)
    record({ output: label })
    expect(label).toBe(expected)
  })
})
