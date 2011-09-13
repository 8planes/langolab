require "rubygems"
require "watir-webdriver"

browser = Watir::Browser.new :firefox
browser.goto "http://www.langolab.com/llauth/login/?next=/enter_conversations/"
browser.text_field(:id, "id_username").set "testuser2"
