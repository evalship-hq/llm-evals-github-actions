import { Mastra } from "@mastra/core"
import { Agent } from "@mastra/core/agent"

export const MODEL = "anthropic/claude-haiku-5-5"
const PROMPT = "Classify the customer support message as billing, bug or other. Reply with that one word only."

/** Replies billing, bug or other to a customer support message. */
const supportAgent = new Agent({ id: "support-agent", name: "support-agent", instructions: PROMPT, model: MODEL })

// The evals take the agent from here (mastra.getAgent), as Mastra's docs advise, not from a direct import.
export const mastra = new Mastra({ agents: { supportAgent } })
