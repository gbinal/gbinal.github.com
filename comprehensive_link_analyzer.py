#!/usr/bin/env python3
"""
Comprehensive link analysis for gbinal.github.com repository
Focuses on internal links and provides detailed external link inventory
"""

import os
import re
import yaml
from urllib.parse import urljoin, urlparse
from pathlib import Path
import json

class ComprehensiveLinkAnalyzer:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.external_links = []
        self.internal_links = []
        self.broken_internal_links = []
        self.template_variables = []
        
    def extract_links_from_markdown(self, content):
        """Extract links from markdown content"""
        links = []
        
        # Markdown links: [text](url)
        md_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
        for text, url in md_links:
            links.append({'type': 'markdown', 'text': text, 'url': url})
        
        # HTML links in markdown: <a href="url">
        html_matches = re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>', content, re.IGNORECASE | re.DOTALL)
        for match in html_matches:
            url, text = match.groups()
            links.append({'type': 'html', 'text': text.strip(), 'url': url})
        
        return links
    
    def extract_links_from_html(self, content):
        """Extract links from HTML content"""
        links = []
        
        # HTML href attributes with context
        html_matches = re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>', content, re.IGNORECASE | re.DOTALL)
        for match in html_matches:
            url, text = match.groups()
            links.append({'type': 'html', 'text': text.strip(), 'url': url})
        
        return links
    
    def extract_links_from_yaml(self, content):
        """Extract links from YAML content (like _config.yml)"""
        links = []
        try:
            data = yaml.safe_load(content)
            
            def extract_from_dict(d, path=""):
                if isinstance(d, dict):
                    for key, value in d.items():
                        current_path = f"{path}.{key}" if path else key
                        if isinstance(value, str) and (value.startswith('http') or value.startswith('//')):
                            links.append({'type': 'yaml', 'text': current_path, 'url': value})
                        elif isinstance(value, (dict, list)):
                            extract_from_dict(value, current_path)
                elif isinstance(d, list):
                    for i, item in enumerate(d):
                        extract_from_dict(item, f"{path}[{i}]")
            
            extract_from_dict(data)
        except yaml.YAMLError:
            pass
        
        return links
    
    def is_external_link(self, url):
        """Check if a link is external"""
        if url.startswith('http://') or url.startswith('https://'):
            return True
        if url.startswith('//'):
            return True
        return False
    
    def is_template_variable(self, url):
        """Check if URL contains template variables"""
        return '{{' in url or '{%' in url
    
    def normalize_internal_link(self, url, current_file_path):
        """Normalize internal links to file paths"""
        # Remove fragments
        url = url.split('#')[0]
        
        # Skip empty URLs
        if not url or url == '/':
            return None
            
        # Handle absolute paths from site root
        if url.startswith('/'):
            # Convert to relative path from repo root
            url = url.lstrip('/')
            
        # Handle relative paths
        else:
            # Make relative to current file's directory
            current_dir = current_file_path.parent
            url = str(current_dir / url)
        
        return url
    
    def check_internal_link(self, url, current_file_path):
        """Check if internal link exists"""
        normalized = self.normalize_internal_link(url, current_file_path)
        if not normalized:
            return True  # Skip empty/root links
        
        # Try different variations
        possible_paths = [
            self.repo_path / normalized,
            self.repo_path / f"{normalized}.md",
            self.repo_path / f"{normalized}.html",
            self.repo_path / normalized / "index.md",
            self.repo_path / normalized / "index.html",
        ]
        
        for path in possible_paths:
            if path.exists() and path.is_file():
                return True
        
        return False
    
    def scan_file(self, file_path):
        """Scan a single file for links"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return
        
        links = []
        
        if file_path.suffix == '.md':
            links = self.extract_links_from_markdown(content)
        elif file_path.suffix in ['.html', '.htm']:
            links = self.extract_links_from_html(content)
        elif file_path.name == '_config.yml':
            links = self.extract_links_from_yaml(content)
        
        for link_info in links:
            url = link_info['url']
            
            # Skip empty links, fragments, and mailto
            if not url or url.startswith('#') or url.startswith('mailto:'):
                continue
            
            link_info['file'] = str(file_path.relative_to(self.repo_path))
            
            if self.is_template_variable(url):
                self.template_variables.append(link_info)
            elif self.is_external_link(url):
                self.external_links.append(link_info)
            else:
                self.internal_links.append(link_info)
                # Check if internal link is broken
                if not self.check_internal_link(url, file_path):
                    self.broken_internal_links.append(link_info)
    
    def scan_repository(self):
        """Scan all files in the repository"""
        print("🔍 Scanning repository for links...")
        
        # Find all relevant files
        patterns = ['**/*.md', '**/*.html', '**/*.htm', '_config.yml']
        files_to_scan = []
        
        for pattern in patterns:
            files_to_scan.extend(self.repo_path.glob(pattern))
        
        print(f"📁 Found {len(files_to_scan)} files to scan")
        
        for file_path in files_to_scan:
            self.scan_file(file_path)
        
        print(f"🌐 Found {len(self.external_links)} external links")
        print(f"🏠 Found {len(self.internal_links)} internal links")
        print(f"🔧 Found {len(self.template_variables)} template variables")
    
    def categorize_external_links(self):
        """Categorize external links by domain"""
        domains = {}
        for link in self.external_links:
            try:
                domain = urlparse(link['url']).netloc.lower()
                if domain not in domains:
                    domains[domain] = []
                domains[domain].append(link)
            except:
                if 'unknown' not in domains:
                    domains['unknown'] = []
                domains['unknown'].append(link)
        
        return domains
    
    def generate_comprehensive_report(self):
        """Generate comprehensive link analysis report"""
        print("\n" + "="*80)
        print("COMPREHENSIVE LINK ANALYSIS REPORT")
        print("Repository: gbinal.github.com")
        print("="*80)
        
        # Internal Links Analysis
        print(f"\n🏠 INTERNAL LINKS ANALYSIS")
        print(f"Total internal links: {len(self.internal_links)}")
        print(f"Broken internal links: {len(self.broken_internal_links)}")
        
        if self.broken_internal_links:
            print(f"\n❌ BROKEN INTERNAL LINKS:")
            for link in self.broken_internal_links:
                print(f"  • {link['url']}")
                print(f"    File: {link['file']}")
                print(f"    Text: '{link['text']}'")
                print()
        else:
            print("✅ All internal links are valid!")
        
        # Template Variables
        if self.template_variables:
            print(f"\n🔧 TEMPLATE VARIABLES (Not actual links):")
            for var in self.template_variables:
                print(f"  • {var['url']} in {var['file']}")
        
        # External Links by Domain
        print(f"\n🌐 EXTERNAL LINKS BY DOMAIN")
        domains = self.categorize_external_links()
        
        for domain, links in sorted(domains.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"\n📍 {domain} ({len(links)} links):")
            for link in links[:5]:  # Show first 5 links per domain
                print(f"  • {link['url']}")
                print(f"    From: {link['file']}")
            if len(links) > 5:
                print(f"    ... and {len(links) - 5} more")
        
        # Summary
        print(f"\n📊 SUMMARY")
        print(f"Total files scanned: {len(set(link['file'] for link in self.external_links + self.internal_links))}")
        print(f"External links: {len(self.external_links)}")
        print(f"Internal links: {len(self.internal_links)}")
        print(f"Broken internal links: {len(self.broken_internal_links)}")
        print(f"Template variables: {len(self.template_variables)}")
        
        # Network testing note
        print(f"\n⚠️  EXTERNAL LINK TESTING LIMITATION")
        print(f"External links cannot be tested in this environment due to network restrictions.")
        print(f"However, the external links have been cataloged above for manual verification.")
        print(f"Most major domains (YouTube, GitHub, Wikipedia, etc.) are likely working.")
        
        # Save detailed report
        self.save_detailed_report()
    
    def save_detailed_report(self):
        """Save detailed report to file"""
        report_data = {
            'external_links': self.external_links,
            'internal_links': self.internal_links,
            'broken_internal_links': self.broken_internal_links,
            'template_variables': self.template_variables
        }
        
        with open('/tmp/link_analysis_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: /tmp/link_analysis_report.json")

def main():
    repo_path = "/home/runner/work/gbinal.github.com/gbinal.github.com"
    
    print("🚀 Starting comprehensive link analysis for gbinal.github.com repository")
    print(f"📂 Repository path: {repo_path}")
    
    analyzer = ComprehensiveLinkAnalyzer(repo_path)
    analyzer.scan_repository()
    analyzer.generate_comprehensive_report()

if __name__ == "__main__":
    main()