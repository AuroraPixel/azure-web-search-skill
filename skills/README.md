# Skills Directory - Web Search Skill Set

This directory contains AI skill definitions specifically for Azure OpenAI Web Search. These skills are exposed as MCP resources through FastMCP Skills Provider.

## 📁 Directory Structure

```
skills/
├── research-assistant/     # Research Assistant skill
│   └── SKILL.md
├── news-analyzer/          # News Analyzer skill
│   └── SKILL.md
└── README.md              # This file
```

## 🎯 Available Skills

### 1. Research Assistant

**File**: `research-assistant/SKILL.md`

**Focus**: Web Search research and analysis

**Core Capabilities**:
- Quick Search - Efficient information retrieval
- Agentic Search - Deep analysis
- Information synthesis and verification
- Source tracking and evaluation

**Use Cases**:
- Technical research
- Market analysis
- Academic research
- Comprehensive research

**Tools Used**:
- `web_search_quick` - Quick search
- `web_search_agentic` - Agentic search

**Typical Workflow**:
```
1. web_search_quick - Understand topic overview
2. web_search_agentic - Deep analysis of key points
3. Generate complete research report
```

### 2. News Analyzer

**File**: `news-analyzer/SKILL.md`

**Focus**: Web Search news analysis

**Core Capabilities**:
- Real-time news search
- Multi-angle analysis
- Trend tracking
- Source evaluation

**Use Cases**:
- Breaking news tracking
- Event deep analysis
- Industry dynamics monitoring
- Trend prediction

**Tools Used**:
- `web_search_quick` - Get latest information
- `web_search_agentic` - Deep analysis

**Typical Workflow**:
```
1. web_search_quick - Get latest reports
2. web_search_agentic - Analyze impact and trends
3. Generate news analysis report
```

## 🚀 Usage

### Access via MCP Client

Skills are exposed as MCP resources, accessible via URIs:

```
skill://research-assistant
skill://news-analyzer
```

### Using in Claude Desktop

1. Claude automatically loads the skill list
2. Ask Claude to use a specific skill:

   ```
   "Use research-assistant skill to research 'quantum computing applications'"
   "Use news-analyzer skill to analyze 'today's tech news'"
   ```

### Using in Cursor

1. Cursor automatically recognizes available skills
2. Mention the skill name in chat to use it

### Direct Skill Documentation

Each skill's SKILL.md file contains complete documentation, read directly for detailed usage.

## 📝 Creating New Skills

To create a new Web Search skill, follow these steps:

### 1. Create Skill Directory

```bash
mkdir skills/your-skill-name
```

### 2. Create SKILL.md

```bash
touch skills/your-skill-name/SKILL.md
```

### 3. Write Skill Content

SKILL.md should include these sections:

```markdown
# Skill Name - Web Search Skill

## Overview
Brief description of skill's purpose and focus

## Capabilities
- Capability 1 (tools used)
- Capability 2

## Use Cases
1. Use case 1
2. Use case 2

## Standard Workflow
### Phase 1: ...
### Phase 2: ...

## Output Format
### Report Template
...

## Best Practices
### ✅ Should Do
### ❌ Should Avoid

## Tool Usage Guide
### web_search_quick
...
### web_search_agentic
...

## Common Use Cases
...

## Version History
- **v1.0.0** (Date): Initial version
```

### 4. Restart MCP Server

After restart, the new skill will be automatically discovered and available.

## 🔍 Skill Manifests

Access skill manifest resources:

```
skill://research-assistant/_manifest
skill://news-analyzer/_manifest
```

Manifests include:
- Skill name
- Version information
- Description
- File list
- Capability list

## 🎯 Design Principles

Our skills focus on **Web Search** core functionality:

### 1. Dual-Mode Strategy

- **Quick Search**: For simple queries and quick information retrieval
- **Agentic Search**: For complex analysis and deep understanding

### 2. Focus Areas

- **Information Research**: Collect, analyze, and synthesize information
- **News Analysis**: Track, analyze, and understand news

### 3. Not Included

- ❌ Code review (not a search scenario)
- ❌ Deep research mode (removed)
- ❌ Other non-search-related functions

## 🔧 Configuration

### Enable/Disable Skills

Skills Provider is configured in `bin/mcp_server.py`:

```python
def setup_skills_provider():
    """Setup Skills Provider"""
    skills_dir = project_root / "skills"

    if skills_dir.exists():
        from fastmcp.server.providers.skills import SkillsDirectoryProvider
        mcp.add_provider(SkillsDirectoryProvider(roots=skills_dir))
```

### Skills Directory Configuration

Default skills directory: `<project_root>/skills`

Can be modified in `setup_skills_provider()`.

## 📊 Skill Comparison

| Skill | Main Purpose | Typical Tools | Output Type |
|-------|-------------|---------------|-------------|
| Research Assistant | Information research | quick + agentic | Research report |
| News Analyzer | News analysis | quick + agentic | News analysis |

## 🛠️ Troubleshooting

### Skill Not Recognized

1. Check directory structure is correct
2. Ensure SKILL.md file exists
3. Restart MCP server
4. Check server logs

### Skill Content Not Displaying

1. Check SKILL.md format is correct
2. Verify Markdown syntax
3. Confirm file encoding is UTF-8

## 📚 Related Documentation

- [FastMCP Complete Guide](../docs/guides/fastmcp-guide.md)
- [MCP Setup Guide](../docs/guides/mcp-setup.md)
- [API Reference](../docs/guides/api-reference.md)
- [Main README](../README.md)

## 🎓 Best Practices

### Using Skills

1. **Choose the Right Skill**
   - Research Assistant → Comprehensive research
   - News Analyzer → News analysis

2. **Follow Recommended Workflow**
   - Start with quick search for overview
   - Then agentic search for deep analysis

3. **Verify Information**
   - Cross-validate key facts
   - Check source reliability
   - Note information timeliness

### Creating Skills

1. **Focus on Search Scenarios**
   - Skills should be designed around Web Search
   - Avoid non-search functions

2. **Clear Workflow**
   - Define clear usage steps
   - Explain when to use which tool

3. **Detailed Documentation**
   - Provide rich examples
   - Explain best practices
   - List limitations and notes

## 📞 Getting Help

If you encounter issues:

1. Check [FastMCP Documentation](https://gofastmcp.com)
2. Check project Issues
3. Submit a new Issue
4. See [Troubleshooting section](#🛠️-troubleshooting)

---

**Last Updated**: 2026-01-29
**Version**: 2.0.0 (Focused on Web Search)
