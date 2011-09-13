require "rubygems"
require "watir-webdriver"

if ENV['HEADLESS']
  require 'headless'
  headless = Headless.new
  headless.start
  at_exit do
    headless.destroy
  end
end


browser = Watir::Browser.new :firefox
browser.goto "http://www.google.com"

