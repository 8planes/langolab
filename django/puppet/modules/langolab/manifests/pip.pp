class langolab::pip($venv, $projectdir) {
  python::pip::requirements { "${projectdir}web/deploy/requirements.txt":
    venv => $venv,
    cwd => "${projectdir}web/deploy/";
  }
}
