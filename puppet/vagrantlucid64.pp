class vagrantlucid64 {
  $projectdir = "/opt/langolab/"
  $venv = "${projectdir}venv"
  
  group { "puppet": ensure => "present"; } ->
  class { 'aptitude': } ->
  class { 'java': } ->
  class { 'activemq': } ->
  class { 'rabbitmq::server': } ->
  class { 'python': } ->
  python::venv { "langolabvenv": path => $venv } ->
  python::pip { "langolabreqs":
    venv => $venv,
    cwd => "${projectdir}web/deploy/",
    requirementsfile => "${projectdir}web/deploy/requirements.txt";
  }
}

class { 'vagrantlucid64': }
