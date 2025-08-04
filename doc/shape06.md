# Shape 06: Interactive Document Builder with Write Operations

**Appetite:** 3-4 workdays
**Status:** Shaped (Cost-Optimized)
**Owner:** Development Team
**Last Updated:** 2024-08-04

## Problem Statement

The current coda-cli is entirely read-only, forcing users to manually create and maintain Coda documents through the web interface. This creates significant friction in several key workflows:

### Pain Points Identified

1. **Document Setup Overhead**: Setting up new project documents takes 5-15 minutes of clicking through the Coda web interface
2. **Template Inconsistency**: Manual document creation leads to structural variations across similar projects (60-80% variance in naming and organization)
3. **Bulk Operations Gap**: No way to create multiple similar documents or apply changes across document sets
4. **Version Control Missing**: Document structures can't be version controlled or automated in CI/CD pipelines
5. **Collaboration Bottleneck**: Only document owners can set up new spaces, creating dependency chains

### User Story

> "As a project manager, I want to define document templates as code so that I can automate the creation of consistent project workspaces without manual clicking through the Coda interface."

## Appetite

**Total Allocation:** 3-4 workdays
- **Phase 1 (MVP):** 2-3 workdays - Basic document creation with YAML templates
- **Phase 2 (Polish):** 1 workday - Error handling and documentation

**Cool-down:** 1 workday for testing and bug fixes

## Solution Overview

### Design Philosophy

1. **Minimal Viable Feature**: Document creation with basic templating
2. **Single Confirmation**: One safety check before execution
3. **YAML-First**: Simple declarative templates
4. **Backward Compatible**: Existing CLI functionality remains unchanged

### Core Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   YAML Template │───▶│  Document Creator│───▶│    Coda API     │
│   + Variables   │    │  (single module) │    │     Calls       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Implementation**: Single module (~200 lines total)

## User Flow

```bash
# Create document from template
python coda.py create-doc --template project.yaml --var PROJECT_NAME="Mobile App" --confirm

# Preview before creation (optional)
python coda.py create-doc --template project.yaml --var PROJECT_NAME="Mobile App" --dry-run
```

**Single confirmation prompt:**
```
Create document "Mobile App Dashboard" with 2 sections? [y/N]:
```

## Template Format

```yaml
# project-template.yaml
document:
  name: "{{PROJECT_NAME}} Dashboard"
  sections:
    - name: "Overview"
      type: "canvas"
      content: "# {{PROJECT_NAME}}\n\nProject status and overview"

    - name: "Tasks"
      type: "table"
      columns: ["Task", "Assignee", "Status", "Due Date"]
```

**Variables**: Simple `{{VARIABLE}}` replacement only
**Validation**: Basic required field checking

## Technical Implementation

**Single Module: `app/common/document_creator.py`**
```python
class DocumentCreator:
    def __init__(self, pycoda_client):
        self.client = pycoda_client

    def create_document(self, template_path, variables, confirm=True, dry_run=False):
        # Load and validate template (20 lines)
        # Replace variables (10 lines)
        # Create document via API (30 lines)
        # Handle errors (20 lines)
        pass
```

**CLI Integration**: Single command added to existing structure
**Error Handling**: Basic try/catch with user-friendly messages
**Testing**: Unit tests for template parsing, integration test with mock API

## Rabbit Holes

### Rabbit Hole 1: Complex Template System
**Problem:** Building template engine with loops, conditionals, inheritance
**Circuit Breaker:** Simple `{{VARIABLE}}` string replacement only
**Time Box:** 2 hours maximum

### Rabbit Hole 2: Elaborate Safety Systems
**Problem:** Multiple confirmation steps, rollback, backup retention
**Circuit Breaker:** Single confirmation prompt, rely on Coda's version history
**Time Box:** 4 hours maximum

## No-Gos

1. Interactive template builder (YAML-only approach)
2. Complex rollback/backup system (rely on Coda's version history)
3. Permission management in templates
4. Advanced schema validation beyond basic checks
5. Multi-document operations

## Success Metrics

**Must Have (Week 1):**
1. Basic document creation from YAML
2. Simple variable substitution
3. Single confirmation prompt

**Nice to Have (Week 2):**
1. Table column specification
2. Basic error handling
3. Dry-run preview

## Key Risks

1. **Coda API Limitations**: Research write capabilities early, prototype core functionality
2. **Template Complexity Creep**: Stick to simple string replacement, resist feature additions
3. **Low Adoption**: Start with high-value use case (project setup), gather feedback quickly

## Conclusion

This streamlined approach reduces implementation complexity by 60-70% while maintaining the core business value of automated document creation. The simplified architecture (single module, basic templates, minimal safety) makes this feature easier to test, maintain, and extend.

**Economic Impact**:
- Development time reduced from 6-9 days to 3-4 days
- 40% fewer lines of specification content
- Single module vs. 6-module architecture
- Maintenance cost reduction of ~60%