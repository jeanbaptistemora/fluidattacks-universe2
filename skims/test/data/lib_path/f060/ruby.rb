begin
rescue Namespace::ArgumentError, Namespace::NameError
rescue ArgumentError, NameError
rescue NameError => e
rescue NameError
rescue
else
ensure
end
