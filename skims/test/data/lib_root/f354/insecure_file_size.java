public class Test {

@Bean(name = "multipartResolver")
public CommonsMultipartResolver multipartResolver() {
  CommonsMultipartResolver multipartResolver = new CommonsMultipartResolver();
  multipartResolver.setMaxUploadSize(657600);
  return multipartResolver;
}


@Bean(name = "multipartResolver")
public CommonsMultipartResolver multipartResolver() {
  CommonsMultipartResolver multipartResolver = new CommonsMultipartResolver();
  int size = 104857600;
  multipartResolver.setMaxUploadSize(size);
  return multipartResolver;
}


@Bean(name = "multipartResolver")
public CommonsMultipartResolver multipartResolver() {
  CommonsMultipartResolver multipartResolver = new CommonsMultipartResolver(); // Sensitive, by default if maxUploadSize property is not defined, there is no limit and thus it's insecure
  return multipartResolver;
}

@Bean
public MultipartConfigElement multipartConfigElement() {
  MultipartConfigFactory factory = new MultipartConfigFactory(); // Sensitive, no limit by default
  return factory.createMultipartConfig();
}
}
