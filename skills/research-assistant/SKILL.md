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
Uses `azure_web_search` tool (mode=`quick`):
- **Speed**: Fast response, seconds to return
- **Features**: No reasoning, direct search results
- **Best For**: Simple queries, fact-checking, quick information retrieval

#### Agentic Search
Uses `azure_web_search` tool (mode=`agentic`):
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
Tool: azure_web_search (mode=quick)
Expected: Quick accurate answer
```

### Case 2: Complex Topic Analysis

```
Query: "Impact of quantum computing on cryptography"
Tool: azure_web_search (mode=agentic)
Expected: In-depth analysis from multiple angles
```

### Case 3: Comprehensive Research

```
Steps:
1. azure_web_search (mode=quick) - Understand topic overview
2. azure_web_search (mode=agentic) - Deep analysis of key points
Expected: Complete research report
```

## Standard Workflow

### Phase 1: Quick Exploration

Use `azure_web_search` (mode=`quick`) to quickly understand the topic:

**Goals**:
- Get topic overview
- Identify key concepts
- Understand basic information

**Outputs**:
- Topic introduction
- Key terminology
- Initial information sources

### Phase 2: Deep Analysis

Use `azure_web_search` (mode=`agentic`) for in-depth analysis:

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

### Should Do

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

### Should Avoid

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

### azure_web_search

**Parameters**:
- `query` (required): Search query string
- `mode` (optional): `quick` or `agentic` (default: `quick`)
- `country` (optional): Country code (US, CN, JP, etc.)

**Best Use Cases**:
- Find specific facts
- Get latest information
- Answer simple questions
- Quick topic browsing

**Examples**:
```
azure_web_search("Python 3.12 new features", mode="quick")
azure_web_search("2026 Spring Festival date", mode="quick", country="CN")
azure_web_search("Applications and challenges of quantum computing in cryptography", mode="agentic")
azure_web_search("Impact of AI on job market", mode="agentic", country="US")
```

## Research Strategies

### Strategy 1: Progressive Research

```
Step 1: quick - Understand topic
Step 2: quick - Find key terms
Step 3: agentic - Deep analysis
Step 4: quick - Verify specific facts
```

### Strategy 2: Comparative Analysis

```
Step 1: quick - Get basic information
Step 2: agentic - Analyze different perspectives
Step 3: Integrate comparison results
```

### Strategy 3: Timeliness Tracking

```
Step 1: quick - Get latest information
Step 2: agentic - Analyze trends and changes
Step 3: quick - Verify specific updates
```

## Common Use Cases

### Technical Research

**Topic**: "Rust vs Go performance comparison"

**Process**:
1. `quick` - Get basic performance data
2. `agentic` - Deep analysis of performance differences
3. `quick` - Find latest benchmarks

**Output**: Complete technical comparison report

### Market Analysis

**Topic**: "2026 electric vehicle market trends"

**Process**:
1. `quick` - Get latest market data
2. `agentic` - Analyze driving factors and challenges
3. Synthesize into market report

**Output**: Comprehensive market analysis

### Academic Research

**Topic**: "Machine learning in medical diagnosis"

**Process**:
1. `quick` - Understand application overview
2. `agentic` - Deep analysis of technical details
3. `quick` - Find latest research papers

**Output**: Academic research summary

## Quality Standards

### Standards for Excellent Research

- **Accuracy**: Information is accurate and reliable
- **Completeness**: Covers main aspects
- **Timeliness**: Information is relatively new
- **Verifiability**: Provides sources
- **Balance**: Multi-angle analysis

### Research Quality Checklist

- [ ] Used appropriate tools?
- [ ] Information sources are reliable?
- [ ] Verified key facts?
- [ ] Tagged timeliness?
- [ ] Provided complete citations?
- [ ] Conclusions based on evidence?

## Configuration Recommendations

### Country Code Settings

For region-specific information, use the `country` parameter:

- `US` - United States information
- `CN` - China information
- `JP` - Japan information
- `GB` - United Kingdom information
- `DE` - Germany information

Examples:
```
azure_web_search("China new energy vehicle policy", mode="quick", country="CN")
azure_web_search("US AI regulation policy", mode="agentic", country="US")
```

## Limitations and Notes

### Tool Limitations

- **Quick Search**: No reasoning, suitable for simple queries
- **Agentic Search**: Requires more time but provides deeper analysis
- **No Deep Research Mode**: Removed, focused on two core search modes

### Usage Recommendations

- Choose tools wisely, avoid overusing agentic search
- Pay attention to information timeliness
- Verify important information
- Cite all sources

## Related Resources

- [Web Search API Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/referencing-material)
- [FastMCP Guide](../../docs/guides/fastmcp-guide.md)
- [MCP Setup Guide](../../docs/guides/mcp-setup.md)

## Version History

- **v2.0.0** (2026-01-29): Removed deep research, focused on web search
- **v1.0.0** (2026-01-29): Initial version
