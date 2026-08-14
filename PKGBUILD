pkgname=filenorm
pkgver=1.3.0
pkgrel=1
pkgdesc="A simple utility to normalize file names"
arch=('any')
url="https://github.com/alanarzumanjan/file-normalizer"
license=('custom')
depends=('python' 'python-unidecode')
makedepends=('python-build' 'python-installer' 'python-wheel')
source=("https://files.pythonhosted.org/packages/source/${pkgname::1}/${pkgname}/${pkgname}-${pkgver}.tar.gz")
sha256sums=('24e7adf67124d92fec5bfef507d2d81a35401b05f139acd027f80ba244ff7d64')

build() {
  cd "$pkgname-$pkgver"
  python -m build --wheel --no-isolation
}

package() {
  cd "$pkgname-$pkgver"
  python -m installer --destdir="$pkgdir" dist/*.whl
}