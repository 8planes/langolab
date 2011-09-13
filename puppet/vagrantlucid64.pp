class vagrantlucid64 {
  $projectdir = "/opt/langolab/"
  $venv = "${projectdir}venv"
  
  group { "puppet": ensure => "present"; } ->
  class { 'aptitude': } ->
  class { 'java':
    distribution => "jdk",
    version => "latest";
  } ->
  class { 'activemq': } ->
  class { 'flashpolicytwistd': } ->
  class { 'python': } ->
  python::venv { "langolabvenv": path => $venv }
}

class { 'vagrantlucid64': }
