#!/usr/bin/env python3
"""Generate Copilot plugin agents from the canonical SDD agent prompts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "agents"
DESTINATION = ROOT / "com.github.copilot" / "agents"

TOOL_ALIASES = {
    "Read": "read",
    "NotebookRead": "read",
    "Grep": "search",
    "Glob": "search",
    "Bash": "execute",
    "Write": "edit",
    "Edit": "edit",
    "MultiEdit": "edit",
    "WebSearch": "web",
    "WebFetch": "web",
}


def parse_frontmatter(text: str, path: Path) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing opening frontmatter delimiter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path}: missing closing frontmatter delimiter")

    frontmatter: dict[str, str] = {}
    description: list[str] = []
    in_description = False
    for line in text[4:end].splitlines():
        if in_description:
            if line.startswith((" ", "\t")):
                description.append(line.strip())
                continue
            in_description = False
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.groups()
        if key == "description" and value in (">", "|", ">-", "|-"):
            in_description = True
        else:
            frontmatter[key] = value.strip().strip("\"'")
    if description:
        frontmatter["description"] = " ".join(description)
    return frontmatter, text[end + 5 :].lstrip("\n")


def copilot_tools(frontmatter: dict[str, str]) -> list[str] | None:
    raw = frontmatter.get("tools")
    if raw is None:
        return None
    tools = [tool.strip() for tool in raw.strip("[]").split(",") if tool.strip()]
    mapped = []
    unknown = []
    for tool in tools:
        mcp_tool = re.fullmatch(r"mcp__([A-Za-z0-9_-]+)__([A-Za-z0-9_-]+)", tool)
        if mcp_tool:
            mapped.append(f"{mcp_tool.group(1)}/{mcp_tool.group(2)}")
        elif tool in TOOL_ALIASES:
            mapped.append(TOOL_ALIASES[tool])
        else:
            unknown.append(tool)
    if unknown:
        raise ValueError(f"unsupported source tool(s): {', '.join(unknown)}")
    return sorted(set(mapped))


def render_agent(source: Path) -> tuple[str, str]:
    frontmatter, body = parse_frontmatter(source.read_text(encoding="utf-8"), source)
    description = frontmatter.get("description", "")
    if not description:
        raise ValueError(f"{source}: missing description")

    name = f"sdd-{source.stem}"
    lines = [
        "---",
        f"name: {name}",
        f"description: {json.dumps(description, ensure_ascii=False)}",
    ]
    tools = copilot_tools(frontmatter)
    if tools is not None:
        lines.append(f"tools: {json.dumps(tools)}")
    lines.extend(["---", ""])

    body = (
        "Copilot adapter: use the available Copilot tools corresponding to the allowed tool "
        "aliases above. If an MCP tool or other host capability mentioned below is unavailable, "
        "say so and use the documented inline fallback; never claim an unavailable action was done.\n\n"
        + body
    )
    body = re.sub(
        r"mcp__([A-Za-z0-9_-]+)__([A-Za-z0-9_-]+)",
        r"\1/\2",
        body,
    )
    if len(body) > 30_000:
        raise ValueError(f"{source}: Copilot agent prompt exceeds the 30,000-character limit")
    output = "\n".join(lines) + body
    if not output.endswith("\n"):
        output += "\n"
    return f"{name}.agent.md", output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated files are stale")
    args = parser.parse_args()

    sources = sorted(SOURCE.glob("*.md"))
    if not sources:
        print(f"error: no canonical agent prompts found under {SOURCE}", file=sys.stderr)
        return 1

    expected: dict[str, str] = {}
    try:
        for source in sources:
            filename, content = render_agent(source)
            expected[filename] = content
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    stale: list[str] = []
    for filename, content in expected.items():
        path = DESTINATION / filename
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(filename)
        else:
            DESTINATION.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")

    if args.check:
        unexpected = sorted(
            path.name for path in DESTINATION.glob("*.agent.md") if path.name not in expected
        )
        stale.extend(unexpected)
        if stale:
            print("error: Copilot agent files are stale or unexpected: " + ", ".join(stale), file=sys.stderr)
            return 1

    print(f"{len(expected)} Copilot agents {'verified' if args.check else 'generated'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
