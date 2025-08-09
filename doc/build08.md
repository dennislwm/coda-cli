# Build 08: Template Registry Core Element

**Target:** TemplateRegistry module (~80 lines)  
**Timeline:** 1 day  

## Core Requirements

- Store template name -> Coda document ID mappings in JSON
- CRUD operations: register, retrieve, list, remove templates
- Handle corrupted JSON gracefully
- Basic input validation

## Implementation

### Core Class Structure

```python
# app/common/template_registry.py
import json
import os
from typing import Optional, Dict

class TemplateRegistry:
    def __init__(self, registry_file: str = "templates.json"):
        self.registry_file = registry_file
        self._templates = self._load_templates()
    
    def register_template(self, name: str, doc_id: str) -> None:
        if not name.strip() or not doc_id.strip():
            raise ValueError("Name and document ID cannot be empty")
        self._templates[name.strip()] = doc_id.strip()
        self._save_templates()
    
    def get_template(self, name: str) -> Optional[str]:
        return self._templates.get(name.strip()) if name.strip() else None
    
    def list_templates(self) -> Dict[str, str]:
        return self._templates.copy()
    
    def remove_template(self, name: str) -> bool:
        name = name.strip()
        if name in self._templates:
            del self._templates[name]
            self._save_templates()
            return True
        return False
    
    def _load_templates(self) -> Dict[str, str]:
        try:
            if not os.path.exists(self.registry_file):
                self._save_empty_registry()
                return {}
            
            with open(self.registry_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return {k.strip(): v.strip() for k, v in data.items() 
                           if isinstance(k, str) and isinstance(v, str) 
                           and k.strip() and v.strip()}
        except (json.JSONDecodeError, IOError):
            pass
        
        self._save_empty_registry()
        return {}
    
    def _save_templates(self) -> None:
        with open(self.registry_file, 'w') as f:
            json.dump(self._templates, f, indent=2)
    
    def _save_empty_registry(self) -> None:
        with open(self.registry_file, 'w') as f:
            json.dump({}, f)
```

## TDD Test Cases

```python
# app/tests/test_template_registry.py
import tempfile
import os
import json
import pytest
from common.template_registry import TemplateRegistry

def test_basic_operations():
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
        registry_file = tmp.name
    
    try:
        registry = TemplateRegistry(registry_file)
        
        # Register and retrieve
        registry.register_template("project-tracker", "doc123")
        assert registry.get_template("project-tracker") == "doc123"
        
        # List templates
        templates = registry.list_templates()
        assert len(templates) == 1
        assert templates["project-tracker"] == "doc123"
        
        # Persistence check
        registry2 = TemplateRegistry(registry_file)
        assert registry2.get_template("project-tracker") == "doc123"
        
        # Remove template
        assert registry2.remove_template("project-tracker") == True
        assert registry2.get_template("project-tracker") is None
        assert len(registry2.list_templates()) == 0
        
    finally:
        if os.path.exists(registry_file):
            os.unlink(registry_file)

def test_error_handling():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp.write('invalid json')
        registry_file = tmp.name
    
    try:
        # Should handle corrupted JSON
        registry = TemplateRegistry(registry_file)
        assert registry.list_templates() == {}
        
        # Input validation
        with pytest.raises(ValueError):
            registry.register_template("", "doc123")
        with pytest.raises(ValueError):
            registry.register_template("test", "")
        
        # Non-existent lookups
        assert registry.get_template("nonexistent") is None
        assert registry.remove_template("nonexistent") == False
        
    finally:
        if os.path.exists(registry_file):
            os.unlink(registry_file)

def test_data_cleanup():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        # Create registry with invalid data
        invalid_data = {
            "good": "doc123",
            "": "empty-key",
            "spaces": "   ",
            123: "numeric-key"
        }
        json.dump(invalid_data, tmp)
        registry_file = tmp.name
    
    try:
        registry = TemplateRegistry(registry_file)
        templates = registry.list_templates()
        
        # Should only keep valid entries
        assert len(templates) == 1
        assert templates["good"] == "doc123"
        
    finally:
        if os.path.exists(registry_file):
            os.unlink(registry_file)
```

## Implementation Timeline

**Day 1 (8 hours):**

- Morning: Core TemplateRegistry class and basic CRUD operations
- Afternoon: Error handling, validation, and comprehensive testing

## Success Criteria

**Must Have:**

- [ ] Register/retrieve/list/remove templates
- [ ] JSON persistence with corruption recovery
- [ ] Input validation for empty names/IDs
- [ ] 90%+ test coverage

**Quality Gates:**

- [ ] All tests pass
- [ ] Handles corrupted JSON gracefully
- [ ] Maintains data integrity

## Economic Impact

**Development Cost:** 1 day (8 hours)  
**Token Savings:** 70% reduction from original design (577 -> 170 lines)  
**Engineering Value:** Simple, focused implementation delivering core business requirements without overengineering
