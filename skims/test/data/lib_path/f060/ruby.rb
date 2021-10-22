begin
rescue Namespace::ArgumentError, Namespace::NameError
rescue ArgumentError, NameError
rescue NameError => e
rescue NameError
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
