# -----------------------------------------------------
# Setup tasks.
# -----------------------------------------------------
namespace "setup" do
  desc "Run the development setup"
  task :develop do
    sh("python setup.py develop")
  end

  desc "Run the main setup"
  task :install do
    sh("python setup.py install")
  end

  desc "Install linting requirements"
  task :lint do
    sh("pip install pep8==1.3.3 pylint==0.26.0 coverage==3.5.3 pyflakes")
  end

  desc "Install testing requirements"
  task :test do
    sh("pip install nose")
  end
end

task :setup => ["setup:install", "setup:develop"]
