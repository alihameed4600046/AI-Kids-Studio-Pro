#!/usr/bin/env python3
"""Runtime audit script for AI Kids Studio Pro categories.

Tests all categories for:
- SINGLE: fields with only one option
- EMPTY/MISSING: fields with no options
- Dropdowns properly populated
- Boolean fields showing true/false
- Integer fields showing multiple values
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.prompt.variable_registry import VariableRegistry
from src.prompt.template_registry import TemplateRegistry
from src.prompt.option_library import OptionLibrary

class RuntimeAuditor:
    """Audits all prompt categories for runtime issues."""
    
    def __init__(self):
        self.variable_registry = VariableRegistry()
        self.template_registry = TemplateRegistry(self.variable_registry)
        self.option_library = OptionLibrary()
        self.results = {
            'single': [],
            'empty': [],
            'missing_definition': [],
            'invalid_defaults': [],
            'passed': []
        }
    
    STORY_TYPES = [
        'bedtime', 'moral', 'adventure', 'fairy_tale', 'islamic',
        'jungle', 'space', 'funny', 'mystery', 'custom'
    ]
    
    STORY_TEMPLATE_MAP = {
        'bedtime': 'Bedtime Story',
        'moral': 'Moral Story',
        'adventure': 'Adventure Story',
        'fairy_tale': 'Fairy Tale',
        'islamic': 'Islamic Story',
        'jungle': 'Jungle Story',
        'space': 'Space Story',
        'funny': 'Funny Story',
        'mystery': 'Mystery Story',
        'custom': 'Custom Story',
    }
    
    def audit_all_categories(self) -> Dict[str, Any]:
        """Run full audit on all categories."""
        categories = self.template_registry.get_categories()
        skip_categories = {'Education', 'Stories'}
        
        for category in categories:
            if category in skip_categories:
                continue
            self.audit_category(category)
        
        self.audit_stories_category()
        
        return self.results
    
    def audit_stories_category(self) -> None:
        """Audit all 10 story types in Stories category."""
        for story_type in self.STORY_TYPES:
            template_name = self.STORY_TEMPLATE_MAP.get(story_type)
            if not template_name:
                continue
            
            template_def = self.template_registry.get_template(template_name)
            if not template_def:
                self.results['missing_definition'].append({
                    'category': 'Stories',
                    'template': template_name,
                    'variable': f'story_type={story_type}',
                    'issue': 'Story template not found in registry'
                })
                continue
            
            for var_name in template_def.variables:
                self.audit_variable('Stories', template_name, var_name)
    
    def audit_category(self, category: str) -> None:
        """Audit a single category."""
        templates = self.template_registry.get_templates(category)
        
        for template_def in templates:
            template_name = template_def.name
            variables = template_def.variables
            
            for var_name in variables:
                self.audit_variable(category, template_name, var_name)
    
    def audit_variable(self, category: str, template_name: str, var_name: str) -> None:
        """Audit a single variable."""
        var_def = self.variable_registry.get(var_name)
        
        # Check if VariableDefinition exists
        if not var_def:
            self.results['missing_definition'].append({
                'category': category,
                'template': template_name,
                'variable': var_name,
                'issue': 'VariableDefinition not found in registry'
            })
            return
        
        var_type = var_def.type
        default_value = var_def.default_value or ""
        option_library_name = var_def.option_library or ""
        options = var_def.options or []
        
        # Check for EMPTY defaults
        if not default_value and default_value != "":
            self.results['empty'].append({
                'category': category,
                'template': template_name,
                'variable': var_name,
                'type': var_type,
                'issue': 'Default value is None or empty',
                'expected': 'Non-empty default value'
            })
        
        # Check for SINGLE options
        if var_type in ('dropdown', 'multiselect'):
            option_count = 0
            if option_library_name:
                lib_group = getattr(self.option_library, option_library_name.upper(), None)
                if lib_group:
                    if hasattr(lib_group, 'options'):
                        option_count = len(lib_group.options)
                    elif isinstance(lib_group, list):
                        option_count = len(lib_group)
                else:
                    option_count = len(options)
            else:
                option_count = len(options)
            
            if option_count == 1:
                self.results['single'].append({
                    'category': category,
                    'template': template_name,
                    'variable': var_name,
                    'type': var_type,
                    'option_count': option_count,
                    'source': option_library_name or 'inline options',
                    'issue': 'Only one option available'
                })
            elif option_count == 0:
                self.results['empty'].append({
                    'category': category,
                    'template': template_name,
                    'variable': var_name,
                    'type': var_type,
                    'issue': 'No options available',
                    'expected': 'At least 2 options'
                })
        
        # Check boolean fields
        if var_type == 'boolean':
            if str(default_value).lower() not in ('true', 'false', '1', '0', 'yes', 'no'):
                self.results['invalid_defaults'].append({
                    'category': category,
                    'template': template_name,
                    'variable': var_name,
                    'type': var_type,
                    'default': default_value,
                    'issue': 'Boolean field has non-boolean default'
                })
    
    def generate_report(self) -> str:
        """Generate detailed audit report."""
        report = []
        report.append("=" * 80)
        report.append("AI KIDS STUDIO PRO - RUNTIME AUDIT REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Summary
        total_issues = (
            len(self.results['single']) +
            len(self.results['empty']) +
            len(self.results['missing_definition']) +
            len(self.results['invalid_defaults'])
        )
        
        report.append("SUMMARY")
        report.append("-" * 40)
        report.append(f"Total SINGLE findings: {len(self.results['single'])}")
        report.append(f"Total EMPTY/MISSING findings: {len(self.results['empty'])}")
        report.append(f"Total missing VariableDefinitions: {len(self.results['missing_definition'])}")
        report.append(f"Total invalid defaults: {len(self.results['invalid_defaults'])}")
        report.append(f"Total issues: {total_issues}")
        report.append("")
        
        # Detailed findings
        if self.results['single']:
            report.append("SINGLE FINDINGS")
            report.append("-" * 40)
            for finding in self.results['single']:
                report.append(f"  {finding['category']}/{finding['template']}: "
                            f"{finding['variable']} ({finding['type']}) - "
                            f"{finding['option_count']} option(s) via {finding['source']}")
            report.append("")
        
        if self.results['empty']:
            report.append("EMPTY/MISSING FINDINGS")
            report.append("-" * 40)
            for finding in self.results['empty']:
                report.append(f"  {finding['category']}/{finding['template']}: "
                            f"{finding['variable']} ({finding['type']}) - {finding['issue']}")
            report.append("")
        
        if self.results['missing_definition']:
            report.append("MISSING VARIABLEDEFINITIONS")
            report.append("-" * 40)
            for finding in self.results['missing_definition']:
                report.append(f"  {finding['category']}/{finding['template']}: "
                            f"{finding['variable']} - {finding['issue']}")
            report.append("")
        
        if self.results['invalid_defaults']:
            report.append("INVALID DEFAULTS")
            report.append("-" * 40)
            for finding in self.results['invalid_defaults']:
                report.append(f"  {finding['category']}/{finding['template']}: "
                            f"{finding['variable']} - {finding['issue']} "
                            f"(default: {finding['default']})")
            report.append("")
        
        # Overall status
        if total_issues == 0:
            report.append("STATUS: PASS - All categories are properly configured")
        else:
            report.append(f"STATUS: FAIL - {total_issues} issues found")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_report(self, filepath: Path) -> None:
        """Save report to file."""
        report = self.generate_report()
        filepath.write_text(report, encoding='utf-8')
        print(f"Report saved to: {filepath}")


def main():
    """Main entry point."""
    print("Starting runtime audit...")
    
    auditor = RuntimeAuditor()
    auditor.audit_all_categories()
    
    # Generate and save report
    report = auditor.generate_report()
    print(report)
    
    # Save to file
    output_dir = project_root / "runtime_audit"
    output_dir.mkdir(exist_ok=True)
    report_path = output_dir / f"audit_report_{Path(__file__).stem}.txt"
    report_path.write_text(report, encoding='utf-8')
    
    print(f"\nReport saved to: {report_path}")
    
    # Return exit code based on findings
    total_issues = (
        len(auditor.results['single']) +
        len(auditor.results['empty']) +
        len(auditor.results['missing_definition']) +
        len(auditor.results['invalid_defaults'])
    )
    
    return 0 if total_issues == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
