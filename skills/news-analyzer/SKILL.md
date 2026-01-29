# News Analyzer - Web Search News Analysis Skill

## Overview

This skill specializes in using Azure OpenAI Web Search for real-time news search, analysis, and tracking. We leverage Quick Search for latest information and Agentic Search for in-depth analysis.

## Capabilities

### 1. Real-Time News Search

Uses `web_search_quick` tool:
- **Fast Retrieval**: Second-level response for latest news
- **Broad Coverage**: Multiple news sources
- **Strong Timeliness**: Latest reports and information

### 2. News Deep Analysis

Uses `web_search_agentic` tool:
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
Tool: web_search_quick
Goal: Quickly get latest information
```

### Case 2: News Event Analysis

```
Topic: "2026 AI policy changes"
Tool: web_search_agentic
Goal: Deep analysis of policy impact
```

### Case 3: Industry Dynamics Monitoring

```
Process:
1. web_search_quick - Get latest industry news
2. web_search_agentic - Analyze trends and changes
Expected: Complete industry dynamics report
```

## Standard Workflow

### Phase 1: Quick Scanning

Use `web_search_quick` to get latest information:

**Goals**:
- Get latest reports
- Identify main events
- Collect key information

**Outputs**:
- News list
- Key facts
- Timeline

### Phase 2: Deep Analysis

Use `web_search_agentic` for in-depth analysis:

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

## 📰 Latest Reports

### 1. [Title]
- **Time**: [Publication time]
- **Source**: [Media name]
- **Link**: [URL]
- **Core Content**: [Summary]
- **Timeliness**: ⭐ Latest

### 2. [Title]
...

## 🔍 Deep Analysis

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

## 📈 Trends and Impact

### Short-term Impact
- Impact 1
- Impact 2

### Long-term Trends
- Trend 1
- Trend 2

### Related Events
- Related event 1
- Related event 2

## 🎯 Key Points

1. Point 1
2. Point 2
3. Point 3

## 📊 Source Reliability

| Source | Reliability | Timeliness | Notes |
|--------|-------------|------------|-------|
| Source1 | ⭐⭐⭐ | Latest | Official statement |
| Source2 | ⭐⭐ | 1 day ago | Industry analysis |
```

## Best Practices

### ✅ Should Do

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

### ❌ Should Avoid

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

### web_search_quick (News Quick Retrieval)

**Best Use Cases**:
- Breaking news tracking
- Latest information retrieval
- Quick event scanning
- Real-time information updates

**Usage Tips**:
```
# Search latest news
web_search_quick("2026 AI news")

# Search specific topic
web_search_quick("Tesla Cybertruck delivery", country="US")

# Search industry dynamics
web_search_quick("China new energy policy", country="CN")
```

### web_search_agentic (News Deep Analysis)

**Best Use Cases**:
- Complex event analysis
- Multi-angle report comparison
- Impact assessment
- Trend prediction

**Usage Tips**:
```
# Analyze policy impact
web_search_agentic("Impact of US AI regulation policy on industry")

# Analyze technology trends
web_search_agentic("Quantum computing development status and challenges")

# Comparative analysis
web_search_agentic("Different companies' positions on AI safety")
```

## News Classification

### By Timeliness

#### Real-time News (Past 1 hour)
- Breaking events
- Instant reports
- Quick updates

**Tool**: `web_search_quick`

#### Latest News (Past 24 hours)
- Daily news
- Important events
- Official statements

**Tool**: `web_search_quick` + `web_search_agentic`

#### Recent News (Past 7 days)
- Weekly summary
- Trend analysis
- Deep reports

**Tool**: `web_search_agentic`

### By Topic

#### Technology News
- Product releases
- Technology breakthroughs
- Company updates

#### Financial News
- Market dynamics
- Company earnings
- Economic data

#### Policy News
- Policy releases
- Regulation changes
- Government statements

#### Social News
- Social events
- Cultural phenomena
- Public issues

## Analysis Strategies

### Strategy 1: Quick Tracking

```
Step 1: quick - Get latest reports
Step 2: quick - Verify key facts
Step 3: quick - Track updates
```

**Best For**: Breaking events, real-time monitoring

### Strategy 2: Deep Analysis

```
Step 1: quick - Quickly understand event
Step 2: agentic - Deep analysis of background
Step 3: quick - Get latest progress
```

**Best For**: Complex events, trend analysis

### Strategy 3: Multi-Source Comparison

```
Step 1: quick - Get broad coverage
Step 2: agentic - Compare different angles
Step 3: agentic - Synthesize analysis
```

**Best For**: Controversial topics, multiple viewpoints

## Common Use Cases

### Use Case 1: Tech News Tracking

**Topic**: "Apple Vision Pro Release"

**Process**:
1. `quick` - Get launch information
2. `agentic` - Analyze product features and impact
3. `quick` - Track market reaction

**Output**: Complete product launch analysis

### Use Case 2: Policy Analysis

**Topic**: "EU AI Act Latest Progress"

**Process**:
1. `quick` - Get latest policy updates
2. `agentic` - Analyze policy content and impact
3. `agentic` - Compare policies across different regions

**Output**: Deep policy analysis report

### Use Case 3: Industry Trends

**Topic**: "2026 Electric Vehicle Market"

**Process**:
1. `quick` - Get latest market data
2. `agentic` - Analyze industry trends and drivers
3. `agentic` - Predict future directions

**Output**: Industry trend analysis report

## Source Evaluation

### Reliability Levels

#### ⭐⭐⭐ High Reliability
- Official news agencies (AP, Reuters, Xinhua)
- Mainstream media (BBC, CNN, Caixin)
- Official government statements
- Company official releases

#### ⭐⭐ Medium Reliability
- Professional industry media
- Major financial media
- Authoritative blogs
- Expert opinions

#### ⭐ Requires Verification
- Social media rumors
- Anonymous sources
- Unofficial statements
- Niche websites

### Evaluation Criteria

- **Accuracy**: Are facts accurate?
- **Timeliness**: Is information latest?
- **Objectivity**: Is there bias?
- **Completeness**: Is information complete?
- **Verifiability**: Can other sources corroborate?

## Region Settings

Use `country` parameter to get region-specific news:

```python
# China news
web_search_quick("China headlines", country="CN")

# US news
web_search_quick("US news", country="US")

# Japan news
web_search_quick("Japan news", country="JP")

# Europe news
web_search_quick("Europe news", country="GB")
```

## Quality Standards

### Standards for Excellent News Analysis

- ✅ **Timeliness**: Information is latest
- ✅ **Accuracy**: Facts are accurate
- ✅ **Comprehensiveness**: Multi-angle coverage
- ✅ **Depth**: Has in-depth analysis
- ✅ **Verifiability**: Sources are reliable

### Analysis Quality Checklist

- [ ] Is information latest?
- [ ] Are sources reliable?
- [ ] Were key facts cross-validated?
- [ ] Were multiple angles analyzed?
- [ ] Were timestamps tagged?
- [ ] Were facts distinguished from opinions?

## Limitations and Notes

### Tool Limitations

- **Quick Search**: Fast information retrieval but no deep analysis
- **Agentic Search**: Deep analysis but requires more time
- **Regional Differences**: Search results may vary by region

### Usage Recommendations

- News changes quickly, pay attention to timeliness
- Cross-validate important information
- Focus on official sources
- Understand media bias
- Maintain objective attitude

## Related Resources

- [News Literacy Guide](../docs/guides/news-literacy.md)
- [Source Evaluation](../docs/guides/source-evaluation.md)
- [MCP Setup Guide](../docs/guides/mcp-setup.md)

## Version History

- **v2.0.0** (2026-01-29): Removed deep research, focused on web search
- **v1.0.0** (2026-01-29): Initial version
