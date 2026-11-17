import { Mastra } from "@mastra/core"
import { Agent } from "@mastra/core/agent"

export const MODEL = "anthropic/claude-haiku-5-5"
const PROMPT = "Classify the customer support message as billing, bug or other. Reply with that one word only."

/** Replies billing, bug or other to a customer support message. */
const supportBot = new Agent({ id: "support-bot", name: "support-bot", instructions: PROMPT, model: MODEL })

export const mastra = new Mastra({ agents: { supportBot } })
