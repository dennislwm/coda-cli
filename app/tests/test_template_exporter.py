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

        # Mock API responses based on real structure
        mock_pycoda.get_doc.return_value = json.dumps(doc_response)
        mock_pycoda.list_sections.return_value = json.dumps(sections_response)

        # Act
        result = exporter.extract_document_structure("M-29VGfvl-")

        # Assert - Focus on business value from real API structure
        assert result["name"] == "TrackMySubs.coda"
        assert result["id"] == "M-29VGfvl-"
        assert len(result["sections"]) == 3
        assert result["sections"][0]["name"] == "Track"
        assert result["sections"][0]["contentType"] == "canvas"
        assert result["sections"][1]["name"] == "History"
        assert result["sections"][2]["name"] == "Summary"

        # Verify correct API calls were made
        mock_pycoda.get_doc.assert_called_once_with("M-29VGfvl-")
        mock_pycoda.list_sections.assert_called_once_with("M-29VGfvl-")

    def test_conservative_variable_detection(self):
        """TemplateExporter should detect variables conservatively using real document patterns"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)
        exporter = TemplateExporter(mock_pycoda)

        # Test Case 1: TrackMySubs.coda - should detect PROJECT_NAME and ENTITY_NAME
        document_structure_1 = {
            "name": "TrackMySubs.coda",
            "sections": [
                {"name": "Track", "contentType": "canvas"},
                {"name": "History", "contentType": "canvas"},
                {"name": "Summary", "contentType": "canvas"}
            ]
        }

        # Act
        variables_1 = exporter.detect_variables(document_structure_1)

        # Assert - Should detect clear patterns from real document
        assert "PROJECT_NAME" in variables_1
        assert variables_1["PROJECT_NAME"] == "TrackMySubs"  # From "TrackMySubs.coda"

        # Test Case 2: PokemonLeesarebest - should detect PROJECT_NAME without .coda
        document_structure_2 = {
            "name": "PokemonLeesarebest",
            "sections": [
                {"name": "Overview", "contentType": "canvas"}
            ]
        }

        variables_2 = exporter.detect_variables(document_structure_2)

        assert "PROJECT_NAME" in variables_2
        assert variables_2["PROJECT_NAME"] == "PokemonLeesarebest"

        # Test Case 3: Question Voting and Polling - should handle multi-word names
        document_structure_3 = {
            "name": "Question Voting and Polling",
            "sections": [
                {"name": "Voting", "contentType": "canvas"}
            ]
        }

        variables_3 = exporter.detect_variables(document_structure_3)

        # Conservative approach: may or may not detect complex multi-word names
        # This tests the conservative boundary condition

        # All test cases should respect Shape 07 constraint
        assert len(variables_1) <= 7
        assert len(variables_2) <= 7
        assert len(variables_3) <= 7

        # Should NOT detect false positives from common section names
        assert "TRACK_NAME" not in variables_1  # Conservative approach
        assert "HISTORY_NAME" not in variables_1
        assert "SUMMARY_NAME" not in variables_1

    def test_generate_yaml_template(self):
        """TemplateExporter should generate DocumentCreator-compatible YAML templates"""
        # Arrange
        mock_pycoda = Mock(spec=Pycoda)
        exporter = TemplateExporter(mock_pycoda)

        # Real document structure from our previous tests
        document_structure = {
            "name": "TrackMySubs.coda",
            "sections": [
                {"name": "Track", "contentType": "canvas"},
                {"name": "History", "contentType": "canvas"},
                {"name": "Summary", "contentType": "canvas"}
            ]
        }

        # Variables detected from our conservative detection
        detected_variables = {"PROJECT_NAME": "TrackMySubs"}

        # Act
        yaml_output = exporter.generate_yaml_template(document_structure, detected_variables)

        # Assert - Must be DocumentCreator compatible
        assert "document:" in yaml_output
        assert "name: \"{{PROJECT_NAME}}.coda\"" in yaml_output
        assert "sections:" in yaml_output
        assert "- name: \"Track\"" in yaml_output
        assert "type: \"canvas\"" in yaml_output

        # Critical: Verify round-trip compatibility
        import yaml
        parsed_template = yaml.safe_load(yaml_output)
        assert "document" in parsed_template
        assert "{{PROJECT_NAME}}" in parsed_template["document"]["name"]
        assert len(parsed_template["document"]["sections"]) == 3

        # Verify sections maintain structure
        track_section = parsed_template["document"]["sections"][0]
        assert track_section["name"] == "Track"
        assert track_section["type"] == "canvas"