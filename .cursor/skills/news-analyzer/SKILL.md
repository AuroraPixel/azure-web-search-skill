---
name: news-analyzer
description: >-
  Search and analyze up-to-date news using Azure OpenAI Web Search (quick/agentic).
  Use for breaking news tracking, multi-source comparison, and trend/impact analysis.
---

# News Analyzer - Web Search News Analysis Skill

## Overview

This skill specializes in using Azure OpenAI Web Search for real-time news search, analysis, and tracking. We leverage Quick Search for latest information and Agentic Search for in-depth analysis.

## Capabilities

### 1. Real-Time News Search

Uses `azure_web_search` tool (mode=`quick`):
- **Fast Retrieval**: Second-level response for latest news
- **Broad Coverage**: Multiple news sources
- **Strong Timeliness**: Latest reports and information

### 2. News Deep Analysis

Uses `azure_web_search` tool (mode=`agentic`):
- **Multi-Angle Analysis**: Understand different media reporting angles
- **Background Analysis**: Analyze deep causes of events
- **Impact Assessment**: Evaluate news impact and significance

### 3. Trend Tracking

- **Event Context**: Track event development process
- **Hotspot Identification**: Identify trending topics
- **Correlation Analysis**: Discover related news

## Use Cases

### Case 1: Breaking News Tracking

```
Event: Major tech company merger
Tool: azure_web_search (mode=quick)
Goal: Quickly get latest information
```

### Case 2: News Event Analysis

```
Topic: "2026 AI policy changes"
Tool: azure_web_search (mode=agentic)
Goal: Deep analysis of policy impact
```

### Case 3: Industry Dynamics Monitoring

```
Process:
1. azure_web_search (mode=quick) - Get latest industry news
2. azure_web_search (mode=agentic) - Analyze trends and changes
Expected: Complete industry dynamics report
```

## Standard Workflow

### Phase 1: Quick Scanning

Use `azure_web_search` (mode=`quick`) to get latest information:

**Goals**:
- Get latest reports
- Identify main events
- Collect key information

**Outputs**:
- News list
- Key facts
- Timeline

### Phase 2: Deep Analysis

Use `azure_web_search` (mode=`agentic`) for in-depth analysis:

**Goals**:
- Analyze reporting angles
- Understand event background
- Evaluate impact and trends

**Outputs**:
- Detailed analysis
- Multi-source comparison
- Predictions and insights

## Output Format

### News Analysis Report Template

```markdown
# News Analysis: [Topic]

## Latest Reports

### 1. [Title]
- **Time**: [Publication time]
- **Source**: [Media name]
- **Link**: [URL]
- **Core Content**: [Summary]
- **Timeliness**: Latest

### 2. [Title]
...

## Deep Analysis

### Event Overview
- **Timeline**: [Development context]
- **Key Facts**: [Main facts]
- **Involved Parties**: [Related parties]

### Reporting Angle Analysis

#### Media Angle A
- **Main Viewpoint**: ...
- **Supporting Evidence**: ...
- **Reporting Style**: ...

#### Media Angle B
...

### Background Analysis
- **Historical Background**: ...
- **Related Events**: ...
- **Deep Causes**: ...

## Trends and Impact

### Short-term Impact
- Impact 1
- Impact 2

### Long-term Trends
- Trend 1
- Trend 2

### Related Events
- Related event 1
- Related event 2

## Key Points

1. Point 1
2. Point 2
3. Point 3

## Source Reliability

| Source | Reliability | Timeliness | Notes |
|--------|-------------|------------|-------|
| Source1 | High | Latest | Official statement |
| Source2 | Medium | 1 day ago | Industry analysis |
```

## Best Practices

### Should Do

1. **Prioritize Quick Search**
   - Quickly get latest news
   - Understand event overview
   - Collect basic information

2. **Verify Information Sources**
   - Cross-validate key facts
   - Check source reliability
   - Distinguish facts from opinions

3. **Focus on Timeliness**
   - Tag publication time
   - Prioritize latest information
   - Note information timeliness window

4. **Multi-Angle Analysis**
   - Compare different media reports
   - Identify reporting bias
   - Synthesize multiple sources

### Should Avoid

1. **Rely on Single Source**
   - Different media have different angles
   - Cross-validation is important

2. **Ignore Timestamps**
   - News changes quickly
   - Check if information is outdated

3. **Confuse Facts and Opinions**
   - Clearly distinguish factual reporting
   - Identify commentary and analysis

4. **Ignore Context**
   - Understand news background
   - Consider historical context

## Tool Usage Guide

### azure_web_search (News Search)

**Best Use Cases**:
- Breaking news tracking
- Latest information retrieval
- Quick event scanning
- Real-time information updates

**Usage Tips**:
```
# Search latest news
azure_web_search("2026 AI news", mode="quick")

# Search specific topic
azure_web_search("Tesla Cybertruck delivery", mode="quick", country="US")

# Search industry dynamics
azure_web_search("China new energy policy", mode="quick", country="CN")
```

For deep analysis, use `mode="agentic"`:
```
azure_web_search("Impact of US AI regulation policy on industry", mode="agentic")
azure_web_search("Quantum computing development status and challenges", mode="agentic")
azure_web_search("Different companies' positions on AI safety", mode="agentic")
```

## Related Resources

- [FastMCP Guide](../../../../docs/guides/fastmcp-guide.md)
- [MCP Setup Guide](../../../../docs/guides/mcp-setup.md)

## Version History

- **v2.0.0** (2026-01-29): Removed deep research, focused on web search
- **v1.0.0** (2026-01-29): Initial version
