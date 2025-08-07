# Shape 07: Automated YAML Template Export

**Appetite:** 2-3 workdays
**Status:** Shaped (Ready for Betting Table)
**Owner:** Development Team
**Last Updated:** 2025-08-07

## Expiration Conditions
- Coda API document structure changes significantly
- Users adopt alternative templating solutions
- DocumentCreator from Shape 06 not completed/modified

## Problem
Users spend 30-45 minutes manually converting existing Coda documents to reusable YAML templates:
1. Export JSON with `get-doc`
2. Analyze complex nested structure
3. Hand-craft YAML with variable placeholders
4. Test template accuracy through trial-and-error

This manual workflow creates adoption barriers and defeats automation benefits.

## Appetite
**Time Estimate**: 2-3 workdays
- Analysis: 0.5 days (JSON-to-YAML patterns)
- Implementation: 1.5 days (export command + variable detection)
- Testing: 0.5-1 days (real document validation)

## Solution
**Core Feature**: `export-template` command converts document ID to ready-to-use YAML template

**Key Capabilities:**
- Intelligent variable detection (PROJECT_NAME, TEAM_NAME, dates)
- Structure preservation (sections, tables, controls)
- Direct compatibility with existing DocumentCreator
- Single command operation

## Implementation Flow
1. `export-template --doc DOC_ID --output template.yaml`
2. Parse document JSON via existing get_doc
3. Detect variables: "Project Alpha Dashboard" → "{{PROJECT_NAME}} Dashboard"
4. Generate YAML template
5. Use immediately: `create-doc --template template.yaml --var PROJECT_NAME="Sales Q2"`

**Architecture**: JSON Export → Pattern Detection → YAML Generation

## Key Constraints
- **Variable Detection**: 5-7 common patterns only (4-hour implementation limit)
- **Structure Support**: Core elements (name, sections, tables) - 80% coverage target
- **Template Features**: Simple substitution only, no advanced templating

## Out of Scope
1. Complex variable types (arrays, nested objects)
2. Content analysis for semantic variables
3. Multi-document templates
4. Template validation/round-trip verification
5. Custom variable naming during export
6. Permission template export
7. Formula preservation (exported as static content)

## Technical Implementation
**Single module**: `app/common/template_exporter.py`
- TemplateExporter class using existing pycoda client
- Pattern detection for common variables
- YAML generation with DocumentCreator compatibility
- CLI integration following existing patterns

## Success Metrics
**Must Have:**
1. Document structure export to YAML
2. Variable detection for names
3. Templates work with DocumentCreator

**Nice to Have:**
1. Table structure preservation
2. 5-7 variable patterns
3. Comment generation for detected variables

## Risks & Mitigation
1. **JSON Complexity**: Start simple, add incrementally (6-hour limit on edge cases)
2. **Variable Accuracy**: Conservative approach, prefer no variable over wrong variable
3. **YAML Quality**: Focus on functional correctness, 80% accuracy acceptable

## Betting Recommendation: **BET - High Value, Low Risk**

**Value**: Eliminates 30-45 minutes manual work per template, removes technical barriers, creates complete templating workflow

**Risk**: Low technical risk (builds on proven components), controlled complexity

**ROI**: Immediate user time savings, positions CLI as comprehensive automation tool

**Fallback**: Reduce to document/section structure only with single variable pattern (1-2 workdays)

## Economic Impact
- **User Savings**: 30-45 minutes → 30 seconds per template
- **Implementation Cost**: 2-3 workdays
- **Maintenance**: Low (single module, simple patterns)
- **ROI**: Immediate upon completion