import pytest
import json
from unittest.mock import Mock
from common.pycoda import Pycoda
from common.template_exporter import TemplateExporter


class TestTemplateExporter:
    """Consolidated tests for TemplateExporter - all functionality in one place"""

    def test_template_exporter_instantiation(self):
        """TemplateExporter should instantiate with a Pycoda instance"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)

        # Act & Assert
        exporter = TemplateExporter(mock_pycoda)

        # Verify the instance was created and has the expected dependency
        assert exporter is not None
        assert hasattr(exporter, 'pycoda')
        assert exporter.pycoda is mock_pycoda

    def test_extract_document_structure(self):
        """TemplateExporter should extract meaningful structure from real Coda API responses"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)
        exporter = TemplateExporter(mock_pycoda)

        # Real Coda API structure based on actual JSON files
        # get_doc returns document metadata
        doc_response = {
            "id": "M-29VGfvl-",
            "name": "TrackMySubs.coda",
            "owner": "dennislwm@gmail.com",
            "ownerName": "Dennis Lee",
            "docSize": {
                "totalRowCount": 1005,
                "tableAndViewCount": 3,
                "pageCount": 3
            }
        }

        # list_sections returns array of section/page objects
        sections_response = [
            {
                "id": "canvas-SuoSR_ZPcM",
                "name": "Track",
                "contentType": "canvas",
                "type": "page"
            },
            {
                "id": "canvas-xh0LObKHSL",
                "name": "History",
                "contentType": "canvas",
                "type": "page"
            },
            {
                "id": "canvas-Ptrr8yunZl",
                "name": "Summary",
                "contentType": "canvas",
                "type": "page"
            }
        ]

        # RED PHASE: list_tables returns array of table objects based on real API structure
        tables_response = [
            {
                "id": "grid-DSbwC3HRoo",
                "type": "table",
                "name": "English Opened Pack", 
                "parent": {
                    "id": "canvas-OfvEDa_Lsg",
                    "name": "English Pack"
                }
            },
            {
                "id": "grid-xyz123",
                "type": "table",
                "name": "Task Table",
                "parent": {
                    "id": "canvas-SuoSR_ZPcM",
                    "name": "Track"
                }
            }
        ]

        # Mock API responses based on real structure
        mock_pycoda.get_doc.return_value = json.dumps(doc_response)
        mock_pycoda.list_sections.return_value = json.dumps(sections_response)
        # RED PHASE: Mock the list_tables API call (will fail because method doesn't exist yet)
        mock_pycoda.list_tables.return_value = json.dumps(tables_response)

        # Act
        result = exporter.extract_document_structure("M-29VGfvl-")

        # Assert - Focus on business value from real API structure
        assert result["name"] == "TrackMySubs.coda"
        assert result["id"] == "M-29VGfvl-"
        # RED PHASE: Expect ownerName to be included in extracted structure (will fail)
        assert result["ownerName"] == "Dennis Lee"
        assert len(result["sections"]) == 3
        assert result["sections"][0]["name"] == "Track"
        assert result["sections"][0]["contentType"] == "canvas"
        assert result["sections"][1]["name"] == "History"
        assert result["sections"][2]["name"] == "Summary"

        # RED PHASE: Expect tables to be included in extracted structure (will fail)
        assert "tables" in result
        assert len(result["tables"]) == 2
        assert result["tables"][0]["name"] == "English Opened Pack"
        assert result["tables"][0]["parent"]["name"] == "English Pack"
        assert result["tables"][1]["name"] == "Task Table"
        assert result["tables"][1]["parent"]["name"] == "Track"

        # Verify correct API calls were made
        mock_pycoda.get_doc.assert_called_once_with("M-29VGfvl-")
        mock_pycoda.list_sections.assert_called_once_with("M-29VGfvl-")
        # RED PHASE: Verify list_tables API call was made (will fail)
        mock_pycoda.list_tables.assert_called_once_with("M-29VGfvl-")

    def test_conservative_variable_detection(self):
        """TemplateExporter should detect variables conservatively using real document patterns"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)
        exporter = TemplateExporter(mock_pycoda)

        # RED PHASE: Test Case 1 - should detect DOC_NAME and OWNER_NAME (not PROJECT_NAME)
        document_structure_1 = {
            "name": "TrackMySubs.coda",
            "ownerName": "Dennis Lee",  # RED PHASE: Add ownerName to document structure
            "sections": [
                {"name": "Track", "contentType": "canvas"},
                {"name": "History", "contentType": "canvas"},
                {"name": "Summary", "contentType": "canvas"}
            ]
        }

        # Act
        variables_1 = exporter.detect_variables(document_structure_1)

        # RED PHASE: Assert - Should detect DOC_NAME and OWNER_NAME (will fail)
        assert "DOC_NAME" in variables_1  # Changed from PROJECT_NAME - will fail
        assert variables_1["DOC_NAME"] == "TrackMySubs"  # From "TrackMySubs.coda"
        assert "OWNER_NAME" in variables_1  # NEW: OWNER_NAME pattern - will fail
        assert variables_1["OWNER_NAME"] == "Dennis Lee"  # From ownerName field

        # RED PHASE: Test Case 2 - PokemonLeesarebest - should detect DOC_NAME without .coda
        document_structure_2 = {
            "name": "PokemonLeesarebest",
            "ownerName": "Dennis Lee",
            "sections": [
                {"name": "Overview", "contentType": "canvas"}
            ]
        }

        variables_2 = exporter.detect_variables(document_structure_2)

        assert "DOC_NAME" in variables_2  # Changed from PROJECT_NAME - will fail
        assert variables_2["DOC_NAME"] == "PokemonLeesarebest"
        assert "OWNER_NAME" in variables_2  # NEW: OWNER_NAME pattern - will fail
        assert variables_2["OWNER_NAME"] == "Dennis Lee"

        # RED PHASE: Test Case 3 - Question Voting and Polling - should handle multi-word names
        document_structure_3 = {
            "name": "Question Voting and Polling",
            "ownerName": "Dennis Lee",
            "sections": [
                {"name": "Voting", "contentType": "canvas"}
            ]
        }

        variables_3 = exporter.detect_variables(document_structure_3)

        # Conservative approach: may or may not detect complex multi-word names
        # But should always detect OWNER_NAME
        assert "OWNER_NAME" in variables_3  # Will fail
        assert variables_3["OWNER_NAME"] == "Dennis Lee"

        # All test cases should respect Shape 07 constraint
        assert len(variables_1) <= 7
        assert len(variables_2) <= 7
        assert len(variables_3) <= 7

        # Should NOT detect false positives from common section names
        assert "TRACK_NAME" not in variables_1  # Conservative approach
        assert "HISTORY_NAME" not in variables_1
        assert "SUMMARY_NAME" not in variables_1

    def test_generate_yaml_template_nested_structure(self):
        """RED PHASE: TemplateExporter should generate nested table structure under sections"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)
        exporter = TemplateExporter(mock_pycoda)

        # Simple document structure with 2 sections and 2 tables
        document_structure = {
            "name": "TrackMySubs.coda",
            "ownerName": "Dennis Lee",
            "sections": [
                {"name": "Track", "contentType": "canvas"},
                {"name": "Summary", "contentType": "canvas"}
            ],
            "tables": [
                {"name": "Task Table", "parent": {"name": "Track"}},
                {"name": "Summary Table", "parent": {"name": "Summary"}}
            ]
        }

        detected_variables = {
            "DOC_NAME": "TrackMySubs"
        }

        # Act
        yaml_output = exporter.generate_yaml_template(document_structure, detected_variables)

        # RED PHASE: Assert nested structure expectations (will fail)
        assert "document:" in yaml_output
        assert "name: '{{DOC_NAME}}.coda'" in yaml_output
        assert "sections:" in yaml_output

        # Should have nested structure
        assert "- name: Track" in yaml_output
        assert "  type: canvas" in yaml_output
        assert "  tables:" in yaml_output  # Tables nested under sections
        assert "  - name: Task Table" in yaml_output

        assert "- name: Summary" in yaml_output
        assert "  tables:" in yaml_output  # Tables nested under sections
        assert "  - name: Summary Table" in yaml_output

        # Should NOT have flat structure
        assert yaml_output.count("tables:") == 2  # Only under sections, not at document level
        assert "parent:" not in yaml_output  # No parent fields in nested structure

        # Verify parsed YAML structure
        import yaml
        parsed_template = yaml.safe_load(yaml_output)
        
        # Should have sections with nested tables
        track_section = None
        summary_section = None
        
        for section in parsed_template["document"]["sections"]:
            if section["name"] == "Track":
                track_section = section
            elif section["name"] == "Summary":
                summary_section = section
        
        # Verify Track section has nested table
        assert track_section is not None
        assert "tables" in track_section
        assert len(track_section["tables"]) == 1
        assert track_section["tables"][0]["name"] == "Task Table"
        assert "parent" not in track_section["tables"][0]  # No parent field in nested structure
        
        # Verify Summary section has nested table
        assert summary_section is not None
        assert "tables" in summary_section
        assert len(summary_section["tables"]) == 1
        assert summary_section["tables"][0]["name"] == "Summary Table"
        assert "parent" not in summary_section["tables"][0]  # No parent field in nested structure

        # Should NOT have document-level tables array
        assert "tables" not in parsed_template["document"]

    def test_sections_without_tables_no_empty_arrays(self):
        """Sections without tables should not have empty tables arrays"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)
        exporter = TemplateExporter(mock_pycoda)

        # Document structure with some sections having tables, others not
        document_structure = {
            "name": "TestDoc.coda",
            "sections": [
                {"name": "Section A", "contentType": "canvas"},  # No tables
                {"name": "Section B", "contentType": "canvas"},  # Has table
                {"name": "Section C", "contentType": "canvas"}   # No tables
            ],
            "tables": [
                {"name": "Table B", "parent": {"name": "Section B"}}
            ]
        }

        detected_variables = {"DOC_NAME": "TestDoc"}

        # Act
        yaml_output = exporter.generate_yaml_template(document_structure, detected_variables)

        # Assert - Verify parsed structure
        import yaml
        parsed = yaml.safe_load(yaml_output)
        
        sections = parsed["document"]["sections"]
        section_a = next(s for s in sections if s["name"] == "Section A")
        section_b = next(s for s in sections if s["name"] == "Section B")
        section_c = next(s for s in sections if s["name"] == "Section C")
        
        # Section A should not have tables key at all
        assert "tables" not in section_a
        
        # Section B should have tables array with one table
        assert "tables" in section_b
        assert len(section_b["tables"]) == 1
        assert section_b["tables"][0]["name"] == "Table B"
        
        # Section C should not have tables key at all
        assert "tables" not in section_c


