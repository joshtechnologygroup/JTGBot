source 'https://rubygems.org'

git_source(:github) do |repo_name|
  repo_name = "#{repo_name}/#{repo_name}" unless repo_name.include?("/")
  "https://github.com/#{repo_name}.git"
end


# Bundle edge Rails instead: gem 'rails', github: 'rails/rails'
gem 'rails', '~> 5.1.3'
# Use sqlite3 as the database for Active Record
gem 'sqlite3'

gem 'rack-cors'

group :development, :test do
  gem 'rspec-rails', '~> 3.6.1'
  gem 'listen', '>= 3.0.5', '< 3.2'
  gem 'puma', '~> 3.7'
  # Call 'byebug' anywhere in the code to stop execution and get a debugger console
  gem 'byebug', platforms: [:mri, :mingw, :x64_mingw]
  gem 'capistrano-rails'
end

group :test do
  gem 'factory_girl_rails', '~> 4.8.0'
end
