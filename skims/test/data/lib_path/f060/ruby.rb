begin
rescue Namespace::ArgumentError, Namespace::NameError
rescue ArgumentError, Exception
rescue ArgumentError, Asdf => e
rescue StandardError
rescue Exception => e
rescue => e
rescue
else
ensure
end

def create_or_update_batch
  @batch ||= begin
    BookBatch.create(book_batch.batch_attrs)
  end
  @batch.update
rescue
  raise_book_batch_error
end
