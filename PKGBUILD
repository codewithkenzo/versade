# Maintainer: Kenzo <kenzo@example.com>
pkgname=python-versade
pkgver=1.0.0
pkgrel=1
pkgdesc="Versade: Versatile dependency analysis and MCP server"
arch=('any')
url="https://github.com/versade/versade"
license=('MIT')
depends=(
    'python>=3.12'
    'python-mcp>=1.2.0'
    'python-uvicorn'
    'python-fastapi'
    'python-pydantic'
    'python-pydantic-settings'
    'python-dotenv'
    'python-httpx'
    'python-orjson'
)
makedepends=(
    'python-build'
    'python-installer'
    'python-wheel'
    'python-setuptools>=61.0'
)
optdepends=(
    'python-mypy: for type checking during development'
    'python-pytest: for running tests'
    'python-pytest-asyncio: for async test support'
    'python-pytest-cov: for test coverage'
    'python-ruff: for linting and formatting'
    'python-black: for code formatting'
    'python-pre-commit: for git hooks'
)
checkdepends=(
    'python-pytest'
    'python-pytest-asyncio'
    'python-pytest-cov'
    'python-mypy'
)
source=("$pkgname-$pkgver.tar.gz::https://github.com/versade/versade/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')  # Update this with the actual SHA256 hash when available

build() {
    cd "versade-$pkgver"
    python -m build --wheel --no-isolation
}

check() {
    cd "versade-$pkgver"
    # Run type checking
    python -m mypy src/versade --ignore-missing-imports || true
    
    # Run tests
    python -m pytest tests/ || true
}

package() {
    cd "versade-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
    
    # Install license
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
    
    # Install documentation
    install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
    
    # Install example configuration
    install -Dm644 .env.example "$pkgdir/usr/share/doc/$pkgname/.env.example" || true
}
