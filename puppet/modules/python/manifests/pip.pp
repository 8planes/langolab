define python::pip($venv, $requirementsfile, $cwd = ".") {
  exec { "$venv/bin/pip install -Ur $requirementsfile":
    cwd => $cwd,
    logoutput => true,
    timeout => 0;
  }
}
