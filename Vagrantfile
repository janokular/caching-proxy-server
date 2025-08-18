Vagrant.configure("2") do |config|
  config.vm.box = "debian/bookworm64"

  config.vm.define "cachingproxy" do |cachingproxy|
    cachingproxy.vm.hostname = "cachingproxy"
    cachingproxy.vm.network "forwarded_port", guest: 3000, host: 3000
  end
end
