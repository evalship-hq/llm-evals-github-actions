import { test } from "vitest"
import { expectEval } from "@mastra/evals/vitest"
import { checks } from "@mastra/evals/checks"
import { mastra } from "../support-agent"

const cases = [
  { id: "double-charge", input: "I was charged twice for my subscription this month.", groundTruth: "billing" },
  { id: "refund-request", input: "Can I get a refund for the annual plan I bought yesterday?", groundTruth: "billing" },
  { id: "app-crash", input: "The app crashes every time I open the settings page.", groundTruth: "bug" },
  { id: "export-error", input: "Exporting a report to CSV fails with a 500 error.", groundTruth: "bug" },
  { id: "dark-mode", input: "Could you add a dark mode?", groundTruth: "other" },
  { id: "support-hours", input: "What are your support hours?", groundTruth: "other" },
]

const hasKey = Boolean(process.env.ANTHROPIC_API_KEY)
if (!hasKey) console.warn("ANTHROPIC_API_KEY is not set, so the evals can't call the model. Skipping them.")

// One test per item: a broken case is one failing test, not a lower pass rate of the whole dataset.
test.skipIf(!hasKey).for(cases)("$id", { timeout: 60_000 }, async ({ input, groundTruth }, { annotate }) => {
  await expectEval({
    target: mastra.getAgent("supportAgent"),
    data: { input, groundTruth },
    // The label alone, whatever its case or the whitespace around it: checks.equals ignores case but doesn't trim.
    gates: [checks.matches(new RegExp(`^\\s*${groundTruth}\\s*$`, "i"))],
    onItemComplete: ({ targetResult }) => annotate(targetResult.text, "output"),
  }).toPass()
})
