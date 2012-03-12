class nginx::apt {
  apt::source { "nginx":
    location => "http://nginx.org/packages/ubuntu/",
    release => "lucid",
    repos => "nginx";
  }
}
