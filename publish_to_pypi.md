# 📦 Publishing Baish to PyPI

This guide provides step-by-step instructions for publishing Baish to PyPI.

## Prerequisites

### 1. PyPI Accounts
- Create account on [PyPI](https://pypi.org/account/register/)
- Create account on [TestPyPI](https://test.pypi.org/account/register/) (for testing)

### 2. API Tokens
- Generate API token on [PyPI](https://pypi.org/manage/account/token/)
- Generate API token on [TestPyPI](https://test.pypi.org/manage/account/token/)
- Store tokens securely (they start with `pypi-`)

### 3. Install Required Tools
```bash
pip install build twine
```

## Publishing Process

### Step 1: Prepare Release

```bash
# 1. Update version in pyproject.toml
# 2. Update CHANGELOG if you have one
# 3. Commit all changes
git add .
git commit -m "Prepare for release v0.1.0"

# 4. Create and push tag
git tag v0.1.0
git push origin v0.1.0
```

### Step 2: Clean and Build

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build source and wheel distributions
python -m build

# Verify build contents
ls -la dist/
# Should see: baish-0.1.0.tar.gz and baish-0.1.0-py3-none-any.whl
```

### Step 3: Test on TestPyPI (Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*
# Enter your TestPyPI API token when prompted

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ baish

# Test the package
baish --help
```

### Step 4: Upload to PyPI

```bash
# Upload to PyPI
twine upload dist/*
# Enter your PyPI API token when prompted
```

### Step 5: Verify Installation

```bash
# Install from PyPI
pip install baish

# Verify it works
baish --help
baish "show my ip address"
```

## Configuration Files for Publishing

### ~/.pypirc (Optional - for easier uploads)

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_API_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TESTPYPI_TOKEN_HERE
```

### Using with twine

```bash
# Upload to TestPyPI using config
twine upload --repository testpypi dist/*

# Upload to PyPI using config
twine upload --repository pypi dist/*
```

## Automated Publishing with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

### Setup GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add new secret: `PYPI_API_TOKEN` with your PyPI API token

### Create Release

1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag: `v0.1.0`
4. Title: `Release v0.1.0`
5. Description: Brief changelog
6. Click "Publish release"

The GitHub Action will automatically build and publish to PyPI.

## Quick Commands Reference

```bash
# Build
python -m build

# Check build
twine check dist/*

# Test upload
twine upload --repository testpypi dist/*

# Production upload
twine upload dist/*

# Install locally for testing
pip install -e .

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ baish

# Install from PyPI
pip install baish
```

## Troubleshooting

### Common Issues

1. **Version already exists**: Update version in `pyproject.toml`
2. **Missing files**: Check `MANIFEST.in` includes all necessary files
3. **Authentication failed**: Verify API token is correct
4. **Build fails**: Check all dependencies are listed in `pyproject.toml`

### Verification Commands

```bash
# Check package metadata
python -m pip show baish

# Verify entry points work
which baish
baish --version

# Test import
python -c "import baish; print('Import successful')"
```

## Post-Publication

1. **Update README badges** with PyPI version
2. **Announce release** on social media/forums
3. **Monitor downloads** on PyPI dashboard
4. **Collect feedback** from users
5. **Plan next release** based on feedback

## Security Notes

- Never commit API tokens to version control
- Use environment variables or GitHub secrets for CI/CD
- Consider using trusted publishers for enhanced security
- Regularly rotate API tokens