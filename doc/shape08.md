# Shape 08: Document Template System

## Expiration
> Conditions for expiry of pitch
- Coda API changes document creation parameters
- Alternative template solutions become available in Coda's native interface
- Team workflow shifts away from document standardization

## Motivation
> Raw idea or anything that motivates this pitch
Teams waste 2-3 hours weekly recreating the same Coda document structures instead of focusing on actual work. The CLI already handles template export but lacks the "create from template" workflow teams need daily.

## Appetite
> Appetite or time for shaping, building and cool-down. Measured in cups of coffee.
```
1. 6 cups of coffee:
   * 2 cups for shaping.
     * Problem validation and solution design using existing API capabilities.
   * 3 cups for building.
     * Implement template registry and document creation commands.
   * 1 cup for cool-down.
```

## Core User-Friendly Solution
> Core elements of user-friendly solution.
- **Template Registry**: Simple JSON mapping of template names to Coda document IDs
- **CLI Commands**: Three commands for registering, listing, and creating from templates
- **Document Creation**: Leverage existing `create_doc()` API with `source_doc` parameter
- **Complete Inheritance**: New documents inherit full structure including tables, formulas, and layouts

## Potential Pitfalls of Core Solution
> Details about user-friendly solution with potential pitfalls or rabbit holes.
- **Source Document Access**: Templates become unusable if source documents are deleted or permissions change
- **Template Versioning**: No version control as templates reference live documents that may change
- **Registry Management**: JSON file corruption or conflicts in team environments
- **API Limitations**: Coda's document copying may not preserve all complex formula relationships

## No-go or Limitations
> Any tasks that will be considered out of scope.
- Template editing interfaces (use Coda's native interface)
- Complex template customization or variable substitution
- Version management for templates
- Template sharing across different Coda accounts
- Automated template discovery or cataloging
