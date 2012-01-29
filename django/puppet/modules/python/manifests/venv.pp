define python::venv($path) {
  exec { "virtualenv $path":
    creates => $path,
    path => "/usr/local/bin:/usr/bin:/bin"
  }
}
