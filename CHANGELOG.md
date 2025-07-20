# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0-dev] - 2025-01-20

### Fixed
- Unicode encoding issues in subprocess calls
- Latin-1 fallback for LaTeX log file reading
- PDF generation reliability improvements

### Changed
- subprocess.run calls now use text=False for binary safety
- Enhanced error reporting for LaTeX compilation failures

## [2.0.0] - 2025-01-20

### Added
- **md2x**: Universal markdown converter supporting multiple formats
- Support for PDF, HTML, DOCX, EPUB, RST, ArXiv formats
- Click-based CLI with improved user experience
- ArXiv-specific package generation
- Workflow automation with Makefile
- GitHub Actions CI/CD workflow
- Comprehensive documentation (IMPROVEMENTS.md, PROJECT_STRUCTURE.md)
- Example files and test suite
- Watch mode for continuous conversion

### Changed
- Package renamed from md2tex to md2x (backward compatible)
- Upgraded to modular architecture with utils package
- Updated all dependencies with version constraints
- Improved error handling and logging
- Enhanced package metadata and classifiers

### Fixed
- Main entry point for direct script execution
- Various edge cases in markdown parsing

### Backward Compatibility
- Original `md2tex` command still available
- All existing functionality preserved
- Can be used as drop-in replacement

## [0.1.0] - Original Release

### Features
- Basic markdown to LaTeX conversion
- Command line interface
- Simple and customizable conversion

---

## Commit History Summary

1. **feat: Add md2x universal markdown converter** (acbf5a4)
   - Core implementation of multi-format converter
   - Modular architecture with utils package

2. **fix: Add main entry point** (901a2e3)
   - Enable direct script execution

3. **build: Upgrade package configuration** (2f1cb13)
   - Modern Python packaging standards
   - Comprehensive metadata

4. **feat: Add workflow automation tools** (7c6e7b6)
   - Makefile for easy conversion
   - Shell scripts for SDPAF paper

5. **docs: Add comprehensive documentation** (93f3a92)
   - IMPROVEMENTS.md
   - PROJECT_STRUCTURE.md
   - README_md2x.md

6. **test: Add test files and debug utilities** (70b89f6)
   - Unit tests
   - Debug helpers

7. **ci: Add GitHub Actions workflow** (a4550f9)
   - Automated testing
   - Build artifacts