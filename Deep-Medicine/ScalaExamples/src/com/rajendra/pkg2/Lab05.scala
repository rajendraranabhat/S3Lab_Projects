package com.rajendra.pkg2

object Lab05 {
  // FIXME
  // define singleton ServerConfiguration
  // with port, host and a method that returns an url

  // TIP
  // Remember that Scala's Uniform Acces Principle means
  // that variables and functions without parameters are
  // accessed in the same way. So you are free to implement
  // the 'url' as method, variable or constant
  def apply(host: String, port: Int) = new ServerConfiguration(host, port)
  def apply() = new ServerConfiguration("localhost", 8080)
}

class ServerConfiguration(val host: String, val port: Int) {
  def url = "http://" + host + ":" + port
}