require "rubygems"
require "watir-webdriver"

browser = Watir::Browser.new :firefox
browser.goto "http://www.google.com"

