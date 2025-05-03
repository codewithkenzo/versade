# Maintainer: Kenzo <kenzo@example.com>
pkgname=python-versade
pkgver=1.0.0
pkgrel=1
pkgdesc="A versatile dependency version checker and documentation finder"
arch=('any')
url="https://github.com/codewithkenzo/versade"
license=('MIT')
depends=('python>=3.12' 'python-fastapi' 'python-uvicorn' 'python-httpx' 'python-orjson' 'python-pydantic')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-setuptools')
optdepends=('python-tomli: for Python <3.11 support')
checkdepends=('python-pytest' 'python-pytest-asyncio' 'python-pytest-cov')
source=("$pkgname-$pkgver.tar.gz::https://github.com/codewithkenzo/versade/archive/v$pkgver.tar.gz")
sha256sums=('SKIP')  # Update this with the actual SHA256 hash when available

build() {
    cd "versade-$pkgver"
    python -m build --wheel --no-isolation
}

check() {
    cd "versade-$pkgver"
    python -m pytest
}

package() {
    cd "versade-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
    install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
}
