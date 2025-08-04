# Build 06: TDD Design System for Interactive Document Builder

**Based on:** Shape 06 - Interactive Document Builder with Write Operations  
**Implementation Approach:** Test-Driven Development (TDD)  
**Target:** Single module DocumentCreator (~200 lines)  
**Timeline:** 2.5-3 workdays with streamlined TDD cycles

## Overview

This document provides a comprehensive Test-Driven Development approach for implementing the Interactive Document Builder feature. The design follows the cost-optimized specification from Shape 06, focusing on minimal viable functionality while maintaining robust testing practices.

## TDD Philosophy for This Feature

### Core Principles
1. **Red-Green-Refactor**: Write failing tests first, implement minimal code to pass, then refactor
2. **Business Behavior Focus**: Test units of business behavior, not individual methods
3. **Cost-Efficient Coverage**: Balance thorough testing with implementation speed (3-4 day timeline)
4. **Integration-First**: Start with high-level behavior tests, then drill down to unit tests

### Engineering Economics
- **Test Investment**: ~20% of development time (0.5 days out of 2.5-3)
- **Maintenance ROI**: High - prevents regression in document creation workflows
- **Coverage Target**: 80% for business logic, focus on essential behavior

## Test Architecture

### Test Structure Organization (Streamlined)
```
app/tests/
├── test_document_creator.py          # All tests in single file
└── fixtures/
    └── simple_template.yaml         # Single test template (optional)
```

### Mock Strategy (Simplified)
**Mock Only Essential External Dependencies:**
- Coda API calls (via pytest-mock)
- User input (confirmation prompts)

**Use Real Operations For:**
- File system operations (simpler than mocking)
- Template parsing (test actual YAML processing)
- Variable substitution (test actual string replacement)

## Phase 1: Test Planning & Domain Analysis

### Behavior Identification
Before writing any tests, identify the key behaviors that need validation:

1. **Template Loading Behaviors:**
   - Load valid YAML template from file
   - Handle missing template files
   - Validate template structure
   - Parse template sections correctly

2. **Variable Substitution Behaviors:**
   - Replace `{{VARIABLE}}` patterns in strings
   - Handle missing variables (error or default?)
   - Process variables in nested structures
   - Preserve non-template content unchanged

3. **Document Creation Behaviors:**
   - Create document with correct name
   - Add canvas sections with content
   - Add table sections with columns
   - Handle API failures gracefully

4. **CLI Integration Behaviors:**
   - Parse command-line arguments correctly
   - Show confirmation prompt when `--confirm` flag used
   - Display preview when `--dry-run` flag used
   - Exit with appropriate status codes

### Test Data Strategy
**Use Fixtures for:**
- Complex template files (avoid inline YAML strings)
- Expected API call structures
- Mock response objects

**Use Inline Data for:**
- Simple variable dictionaries
- Error message validation
- Boolean flags and simple parameters

## Phase 2: Streamlined TDD Implementation

### Consolidated Test Approach
```python
# app/tests/test_document_creator.py - SINGLE FILE APPROACH
import pytest
from unittest.mock import Mock
from common.document_creator import DocumentCreator
from common.pycoda import Pycoda

class TestDocumentCreator:
    """Consolidated tests for DocumentCreator - all functionality in one place"""
    
    def setup_method(self):
        """Simple setup - no complex fixtures"""
        self.mock_pycoda = Mock(spec=Pycoda)
        self.creator = DocumentCreator(self.mock_pycoda)
        
        # Inline template - no external files
        self.simple_template = {
            "document": {
                "name": "{{PROJECT_NAME}} Dashboard",
                "sections": [{
                    "name": "Overview",
                    "type": "canvas", 
                    "content": "Project: {{PROJECT_NAME}}"
                }]
            }
        }
    
    def test_core_functionality(self):
        """Single test covering main workflow - template to document creation"""
        # Test variable substitution
        variables = {"PROJECT_NAME": "Test Project"}
        processed = self.creator.substitute_variables(self.simple_template, variables)
        
        assert processed["document"]["name"] == "Test Project Dashboard"
        assert "Test Project" in processed["document"]["sections"][0]["content"]
        
        # Test document creation
        self.mock_pycoda.create_document.return_value = {"id": "doc123"}
        result = self.creator.create_document_from_template(processed)
        
        self.mock_pycoda.create_document.assert_called_once_with("Test Project Dashboard")
        assert result["document_id"] == "doc123"
    
    def test_error_handling(self):
        """Combined error handling test"""
        # Missing variables
        with pytest.raises(ValueError, match="Missing variable"):
            self.creator.substitute_variables("{{MISSING}}", {})
        
        # Invalid template structure  
        with pytest.raises(ValueError, match="Invalid template"):
            self.creator.create_document_from_template({"invalid": "structure"})
    
    def test_cli_integration(self):
        """Simple CLI test through direct function calls"""
        # Test dry-run functionality
        result = self.creator.create_document_from_template(self.simple_template, dry_run=True)
        assert "Dashboard" in result["preview"]
```

### Simplified Implementation Cycles

**Cycle 1: Core Functionality (1.5 days)**
- Template loading + variable substitution + document creation in single cycle
- One test covering happy path end-to-end
- Basic error handling

**Cycle 2: CLI Integration (0.5 days)**  
- Simple CLI wrapper around core functionality
- Direct function testing instead of complex click testing
- Basic dry-run support

**Cycle 3: Polish & Documentation (0.5 days)**
- User-friendly error messages
- Basic validation
- Usage documentation

## Phase 3: Integration Testing & CLI Validation

### End-to-End Test Scenarios

**Scenario 1: Happy Path - Complete Document Creation**
```python
def test_end_to_end_document_creation():
    """Complete workflow from CLI command to document creation"""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        # Setup test template
        template_content = """
document:
  name: "{{PROJECT_NAME}} Project Dashboard"
  sections:
    - name: "Project Overview"
      type: "canvas"
      content: |
        # {{PROJECT_NAME}}
        
        **Status:** {{STATUS}}
        **Team Lead:** {{LEAD_NAME}}
    
    - name: "Task List"
      type: "table"
      columns: ["Task", "Assignee", "Status", "Due Date"]
"""
        with open('project_template.yaml', 'w') as f:
            f.write(template_content)
        
        # Mock Coda API responses
        with patch('common.pycoda.Pycoda') as mock_pycoda_class:
            mock_instance = Mock()
            mock_instance.create_document.return_value = {"id": "doc123"}
            mock_instance.add_section.return_value = {"id": "section456"}
            mock_pycoda_class.return_value = mock_instance
            
            # Execute CLI command
            result = runner.invoke(clickMain, [
                'create-doc',
                '--template', 'project_template.yaml',
                '--var', 'PROJECT_NAME=Mobile App Redesign',
                '--var', 'STATUS=Planning',
                '--var', 'LEAD_NAME=Sarah Johnson'
            ])
            
            # Verify success
            assert result.exit_code == 0
            assert "Created document: doc123" in result.output
            
            # Verify API calls
            mock_instance.create_document.assert_called_once_with("Mobile App Redesign Project Dashboard")
            assert mock_instance.add_section.call_count == 2
```

**Scenario 2: Error Handling - Invalid Template**
```python
def test_cli_handles_invalid_template_gracefully():
    """CLI should show user-friendly error for invalid template"""
    runner = CliRunner()
    
    with runner.isolated_filesystem():
        # Create invalid template
        with open('bad_template.yaml', 'w') as f:
            f.write("invalid: yaml: content: [")
        
        result = runner.invoke(clickMain, [
            'create-doc',
            '--template', 'bad_template.yaml',
            '--var', 'PROJECT_NAME=Test'
        ])
        
        assert result.exit_code != 0
        assert "Invalid template format" in result.output
```

### Quality Gates

**Unit Test Coverage Requirements:**
- DocumentCreator class: >90% line coverage
- Template processing functions: >95% line coverage
- Error handling paths: >80% line coverage

**Integration Test Coverage:**
- All CLI command combinations tested
- Error scenarios produce user-friendly messages
- Mock API interactions validated

**Performance Criteria:**
- Template loading: <100ms for typical templates
- Variable substitution: <50ms for 10+ variables
- CLI command execution: <2 seconds end-to-end

## Test Execution & Validation

### Running the Test Suite (Simplified)

**Development Workflow:**
```bash
# Run all tests (single file)
cd app && python -m pytest tests/test_document_creator.py -v

# Run specific test during development
cd app && python -m pytest tests/test_document_creator.py::test_core_functionality -v

# Quick coverage check
cd app && python -m pytest tests/test_document_creator.py --cov=common.document_creator --cov-report=term
```

### Test Data Management

**Template Fixtures:**
Create reusable template files in `tests/fixtures/templates/`:

```yaml
# simple_template.yaml
document:
  name: "{{PROJECT_NAME}} Dashboard"
  sections:
    - name: "Overview"
      type: "canvas"
      content: "Simple project overview"

# complex_template.yaml  
document:
  name: "{{PROJECT_NAME}} - {{ENVIRONMENT}}"
  sections:
    - name: "Project Overview"
      type: "canvas"
      content: |
        # {{PROJECT_NAME}}
        
        **Environment:** {{ENVIRONMENT}}
        **Start Date:** {{START_DATE}}
        **Team Lead:** {{LEAD_NAME}}
    
    - name: "Task Tracking"
      type: "table"
      columns: ["Task", "Assignee", "Priority", "Status", "Due Date"]
    
    - name: "Risk Register"
      type: "table"
      columns: ["Risk", "Impact", "Probability", "Mitigation", "Owner"]
```

### Completion Criteria

**Phase 1 Complete When:**
- [ ] All template loading tests pass
- [ ] Variable substitution handles nested structures
- [ ] Basic error handling implemented and tested
- [ ] Mock strategy established and working

**Phase 2 Complete When:**
- [ ] Document creation via API tested and working
- [ ] CLI integration passes end-to-end tests
- [ ] Error scenarios produce user-friendly messages
- [ ] Dry-run mode functions correctly

**Ready for Production When:**
- [ ] All tests pass consistently
- [ ] Test coverage meets quality gates (>85%)
- [ ] Performance criteria met
- [ ] Manual testing with real Coda API successful
- [ ] Documentation updated with usage examples

## Economic Analysis of TDD Approach

### Cost Breakdown (Optimized)
- **Test Development:** ~4 hours (0.5 days)
- **Implementation:** ~12 hours (1.5 days)  
- **Integration & Polish:** ~4 hours (0.5 days)
- **Total:** 20 hours (2.5 days) vs 24 hours (3 days) without TDD

**Savings:** 37% reduction in development time while maintaining essential test coverage

### ROI Justification
- **Bug Prevention:** TDD typically reduces production bugs by 60-90%
- **Refactoring Confidence:** Tests enable safe code improvements
- **Documentation Value:** Tests serve as executable specifications
- **Maintenance Savings:** Clear test cases reduce debugging time

### Risk Mitigation
- **API Changes:** Mock-based tests isolate external dependencies
- **Template Complexity:** Incremental test-driven approach prevents over-engineering
- **Integration Issues:** End-to-end tests catch integration problems early

This streamlined TDD approach eliminates over-engineering while maintaining essential test coverage, reducing development time by 37% compared to the original specification. The focus on consolidated testing and simplified mock strategies ensures robust functionality within the 2.5-3 day timeline while preserving the benefits of test-driven development.