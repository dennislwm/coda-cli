# Build 07: TDD Design - Automated YAML Template Export

**Based on:** Shape 07 - Automated YAML Template Export  
**Target:** TemplateExporter module (~150-200 lines)  
**Timeline:** 2-3 workdays  
**Dependencies:** DocumentCreator, Pycoda get_doc API

## TDD Approach

### Core Principles
- **Red-Green-Refactor** cycles focused on business behavior
- **Conservative scope**: 5-7 variable patterns maximum  
- **Integration-first**: Test export workflow, then pattern detection
- **85% coverage** for business logic, focus on essential behaviors

### Test Architecture
```
app/tests/
├── test_template_exporter.py        # Single consolidated test file
└── fixtures/
    ├── sample_document.json         # Real document structure
    └── expected_template.yaml       # Output validation
```

**Mock Strategy:**
- Mock: Coda API calls, file operations
- Use Real: JSON parsing, variable detection, YAML generation

## Key Business Behaviors

### 1. Document Processing
- Extract document structure from get_doc JSON
- Handle missing/malformed data gracefully
- Preserve section hierarchy and table definitions

### 2. Variable Detection (Conservative)
**Target Patterns (5-7 maximum):**
- PROJECT_NAME: Document titles with "Dashboard", "Project", "Plan"
- TEAM_NAME: Section headers with "Team", "Department"  
- STATUS: Common values ("Planning", "Active", "Complete")
- START_DATE/END_DATE: Standard date patterns
- LEAD_NAME: Person names in consistent positions
- ENVIRONMENT: "Production", "Staging", "Development"

**Detection Rules:**
- Prefer precision over recall (no false positives)
- Max 3-word project names
- Filter common words ("The", "A", "An")

### 3. YAML Generation
- Generate DocumentCreator-compatible templates
- Include variable substitution syntax `{{VARIABLE}}`
- Preserve document metadata and structure
- Validate round-trip compatibility

### 4. CLI Integration
- export-template command following coda.py patterns
- Handle file permissions and output paths
- Display meaningful progress messages

## Implementation Phases

**Phase 1 (1 day):** Core document processing + basic variable detection
**Phase 2 (0.8 days):** Complete variable patterns + conservative algorithms  
**Phase 3 (0.6 days):** CLI integration + error handling

## Essential Test Examples

```python
# Consolidated test approach - key patterns only
class TestTemplateExporter:
    def setup_method(self):
        self.mock_pycoda = Mock(spec=Pycoda)
        self.exporter = TemplateExporter(self.mock_pycoda)
        
    def test_end_to_end_export_workflow(self):
        """Critical: Complete export process"""
        # Mock document with realistic structure
        sample_doc = {
            "name": "Project Alpha Dashboard",
            "sections": [{
                "name": "Alpha Team Tasks",
                "type": "table",
                "content": "Lead: Sarah Johnson\nStatus: Planning"
            }]
        }
        self.mock_pycoda.get_doc.return_value = json.dumps(sample_doc)
        
        # Act: Full export workflow
        yaml_output = self.exporter.export_template("doc123")
        
        # Assert: Business requirements
        assert "{{PROJECT_NAME}}" in yaml_output
        assert "{{LEAD_NAME}}" in yaml_output
        assert DocumentCreator.validate_template(yaml_output)
        
    def test_conservative_variable_detection(self):
        """Critical: No false positives in pattern matching"""
        content = "Project Alpha Dashboard\nTeam Lead: Sarah\nStatus: Planning"
        
        variables = self.exporter.detect_variables(content)
        
        assert variables["PROJECT_NAME"] == "Alpha"
        assert variables["LEAD_NAME"] == "Sarah"
        assert len(variables) <= 7  # Shape 07 constraint
```

## Quality Gates

**Coverage Requirements:**
- TemplateExporter: >90% line coverage
- Variable detection: >95% coverage (critical business logic)
- Round-trip compatibility: 100% success rate

**Performance Targets:**
- Export time: <5 seconds for typical documents
- Variable detection accuracy: >90% precision, <10% false positives

## Completion Criteria

**Ready for Production:**
- [ ] All tests pass consistently (>95% success rate)
- [ ] CLI export-template command works end-to-end
- [ ] Round-trip validation: Export → DocumentCreator workflow successful
- [ ] Performance meets <5 second target
- [ ] Conservative variable detection prevents false positives

## Economic Impact

**Development Cost:** 2.75 days (TDD overhead: 8% vs non-TDD)
**User Value:** Eliminates 30-45 minutes manual work per template
**Risk Mitigation:** Conservative approach prevents user frustration from incorrect templates

**ROI Justification:** Quality assurance through systematic testing enables safe future enhancements while ensuring generated templates work correctly with DocumentCreator on first use.

## Success Factors

- **Focus on business behavior**, not implementation details
- **Conservative engineering**: Better to miss variables than create wrong ones
- **Structure preservation**: Maintain document hierarchy and table definitions
- **Compatibility first**: Every template must work with DocumentCreator

This TDD approach delivers maximum user value within the 2-3 workday constraint through focused testing of essential behaviors and conservative variable detection.