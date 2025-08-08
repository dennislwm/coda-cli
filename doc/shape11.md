# Shape 11: Collection Performance Dashboard

## Expiration
> Conditions for expiry of pitch
- Existing calculated columns in template change significantly
- Coda implements native dashboard functionality that replaces this need
- Collection tracking shifts to different data structure

## Motivation
> Raw idea or anything that motivates this pitch
Rich calculated columns exist (PR SIR%, Avg Value, Total Value) but no consolidated view to understand collection performance. Investment decisions are based on fragmented data instead of clear insights, leaving valuable analytics trapped in individual tables.

## Appetite
> Appetite or time for shaping, building and cool-down. Measured in cups of coffee.
```
1. 8 cups of coffee:
   * 3 cups for shaping.
     * Dashboard design and aggregation strategy using existing metrics.
   * 4 cups for building.
     * Cross-table analysis, dashboard generation, export functionality.
   * 1 cup for cool-down.
```

## Core User-Friendly Solution
> Core elements of user-friendly solution.
- **Performance Summary**: Single consolidated view of key ROI metrics from existing calculations
- **Cross-Collection Analysis**: English vs Japanese performance comparison
- **Export Functionality**: CSV download for historical tracking and external analysis
- **Existing Data Leverage**: Use current PR SIR%, Avg Diff, Total Value calculations without modification

## Potential Pitfalls of Core Solution
> Details about user-friendly solution with potential pitfalls or rabbit holes.
- **Dashboard Complexity**: Too many metrics could overwhelm users and reduce clarity
- **Performance Issues**: Large datasets may cause slow dashboard generation times
- **Data Staleness**: Dashboard may become outdated without regular refresh mechanisms
- **Cross-Table Dependencies**: Changes to original table structures could break aggregation logic

## No-go or Limitations
> Any tasks that will be considered out of scope.
- Advanced charting beyond Coda's native capabilities
- Real-time streaming analytics (batch analysis sufficient)
- Complex machine learning predictions or forecasting
- Integration with external BI tools or platforms
- Modification of existing calculated column formulas
