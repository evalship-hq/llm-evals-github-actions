import { expect, test } from "vitest"
import { classify } from "../support-bot"

const cases = [
  { id: "double-charge", message: "I was charged twice for my subscription this month.", expected: "billing" },
  { id: "refund-request", message: "Can I get a refund for the annual plan I bought yesterday?", expected: "billing" },
  { id: "app-crash", message: "The app crashes every time I open the settings page.", expected: "bug" },
  { id: "export-error", message: "Exporting a report to CSV fails with a 500 error.", expected: "bug" },
  { id: "dark-mode", message: "Could you add a dark mode?", expected: "other" },
  { id: "support-hours", message: "What are your support hours?", expected: "other" },
]

const hasKey = Boolean(process.env.OPENAI_API_KEY)
if (!hasKey) console.warn("OPENAI_API_KEY is not set, so the evals can't call the model. Skipping them.")

test.skipIf(!hasKey).for(cases)("$id", async ({ message, expected }, { annotate }) => {
  const label = await classify(message)
  await annotate(label, "output")
  expect(label).toBe(expected)
}, 30_000)
