class vagrantlucid64 {
  $projectdir = "/opt/langolab/"
  $venv = "${projectdir}venv"
  
  group { "puppet": ensure => "present"; } ->
  class { 'aptitude': } ->
  class { 'java': } ->
  class { 'activemq': } ->
  class { 'flashpolicytwistd': } ->
  class { 'python': } ->
  python::venv { "langolabvenv": path => $venv } ->
  python::pip { "langolabreqs":
    venv => $venv,
    requirementsfile => "${projectdir}web/deploy/requirements.txt";
  }
}

class { 'vagrantlucid64': }
