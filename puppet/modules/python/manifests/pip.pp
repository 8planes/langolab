define python::pip($venv, $requirementsfile) {
  exec { "$venv/bin/pip install -Ur $requirementsfile":
    cwd => $venv
  }
}
