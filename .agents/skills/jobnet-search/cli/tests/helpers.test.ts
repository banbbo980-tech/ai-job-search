import { describe, expect, test } from "bun:test"
import { stripHtml } from "../src/helpers"

describe("stripHtml", () => {
  test("removes tags, decodes common entities, and collapses whitespace", () => {
    const html = "<p>Senior&nbsp;Developer &amp; Tech Lead</p><p>Use &lt;API&gt; tools</p>"

    expect(stripHtml(html)).toBe("Senior Developer & Tech Lead Use <API> tools")
  })
})
