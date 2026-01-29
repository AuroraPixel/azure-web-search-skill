---
name: research-assistant
description: >-
  Research and synthesize information using Azure OpenAI Web Search (quick/agentic).
  Use for fact-finding, technical research, comparative analysis, and source-backed summaries.
---

# Research Assistant - Web Search Skill

## Overview

This skill specializes in using Azure OpenAI Web Search for efficient information collection and analytical research. We focus on two search modes: Quick Search and Agentic Search.

## Capabilities

### 1. Dual-Mode Search

#### Quick Search
Uses `web_search_quick` tool:
- **Speed**: Fast response, seconds to return
- **Features**: No reasoning, direct search results
- **Best For**: Simple queries, fact-checking, quick information retrieval

#### Agentic Search
Uses `web_search_agentic` tool:
- **Speed**: Medium, requires reasoning time
- **Features**: AI reasoning analysis, synthesizes multiple sources
- **Best For**: Complex queries, multi-step reasoning, deep analysis

### 2. Information Processing

- **Source Tracking**: Automatically records all citation sources
- **Information Synthesis**: Integrates information from multiple sources
- **Timeliness Validation**: Tags information publication time
- **Reliability Assessment**: Evaluates source credibility

## Use Cases

### Case 1: Quick Information Lookup

```
Query: "Python 3.12 release date"
Tool: web_search_quick
Expected: Quick accurate answer
```

### Case 2: Complex Topic Analysis

```
Query: "Impact of quantum computing on cryptography"
Tool: web_search_agentic
Expected: In-depth analysis from multiple angles
```

### Case 3: Comprehensive Research

```
Steps:
1. web_search_quick - Understand topic overview
2. web_search_agentic - Deep analysis of key points
Expected: Complete research report
```

## Standard Workflow

### Phase 1: Quick Exploration

Use `web_search_quick` to quickly understand the topic:

**Goals**:
- Get topic overview
- Identify key concepts
- Understand basic information

**Outputs**:
- Topic introduction
- Key terminology
- Initial information sources

### Phase 2: Deep Analysis

Use `web_search_agentic` for in-depth analysis:

**Goals**:
- Understand complex relationships
- Analyze different viewpoints
- Evaluate evidence quality

**Outputs**:
- Detailed analysis
- Multi-angle comparison
- Reliable conclusions

## Output Format

### Research Report Template

```markdown
# Research Topic: [Topic Name]

## Overview
[Brief overview from quick search]

## Key Findings

### Finding 1: [Title]
- **Content**: Detailed description
- **Source**: [Source 1]
- **Timeliness**: [Time information]

### Finding 2: [Title]
...

## Different Perspectives

### Perspective A
- **Supporting Evidence**: ...
- **Main Sources**: ...

### Perspective B
...

## Conclusions

Based on the above research, the main conclusions are:
- Conclusion 1
- Conclusion 2

## References

1. [Source 1](URL) - [Brief description]
2. [Source 2](URL) - [Brief description]
...

## Information Timeliness

- Latest information: [Date]
- Main source time range: [Range]
```

## Best Practices

### ✅ Should Do

1. **Start with Quick Search**
   - Understand topic overview first
   - Identify key terminology
   - Determine research direction

2. **Choose Tools Wisely**
   - Simple queries → quick
   - Complex queries → agentic
   - Comprehensive research → combine both

3. **Verify Information**
   - Cross-validate key facts
   - Check source reliability
   - Confirm information timeliness

4. **Record Sources**
   - Save all citations
   - Tag publication time
   - Evaluate source credibility

### ❌ Should Avoid

1. **Overuse Agentic Search**
   - Simple queries don't need reasoning
   - Wastes time and resources

2. **Ignore Source Verification**
   - Don't trust single sources
   - Verify information accuracy

3. **Neglect Timeliness**
   - Old information may be outdated
   - Pay attention to publication time

4. **Mix Query Types**
   - Focus on one topic at a time
   - Avoid overly broad queries

## Tool Usage Guide

### web_search_quick

**Parameters**:
- `query` (required): Search query string
- `country` (optional): Country code (US, CN, JP, etc.)

**Best Use Cases**:
- Find specific facts
- Get latest information
- Answer simple questions
- Quick topic browsing

**Examples**:
```
web_search_quick("Python 3.12 new features")
web_search_quick("2026 Spring Festival date", country="CN")
```

### web_search_agentic

**Parameters**:
- `query` (required): Search query string
- `country` (optional): Country code

**Best Use Cases**:
- Complex problem analysis
- Multi-step reasoning tasks
- Synthesize multiple sources
- Understand context

**Examples**:
```
web_search_agentic("Applications and challenges of quantum computing in cryptography")
web_search_agentic("Impact of AI on job market", country="US")
```

## Related Resources

- [FastMCP Guide](../../../../docs/guides/fastmcp-guide.md)
- [MCP Setup Guide](../../../../docs/guides/mcp-setup.md)

## Version History

- **v2.0.0** (2026-01-29): Removed deep research, focused on two core search modes
- **v1.0.0** (2026-01-29): Initial version
