# Class: rabbitmq::service
#
#   This class manages the rabbitmq server service itself.
#
#   Jeff McCune <jeff@puppetlabs.com>
#
#
# Parameters:
#
# Actions:
#
# Requires:
#
# Sample Usage:
#
class rabbitmq::service(
  $service_name = 'rabbitmq-server',
  $ensure='running'
) {

  $service_name_real = $service_name

  if $ensure == 'running' {
    Class['rabbitmq::service'] -> Rabbitmq_user<| |>
    Class['rabbitmq::service'] -> Rabbitmq_vhost<| |>
    Class['rabbitmq::service']  -> Rabbitmq_user_permissions<| |>
    $ensure_real = 'running'
    $enable_real = true
  } else {
    $ensure_real = 'stopped'
    $enable_real = false
  }

  service { $service_name_real:
    ensure     => $ensure_real,
    enable     => $enable_real,
    hasstatus  => true,
    hasrestart => true,
  }

}
