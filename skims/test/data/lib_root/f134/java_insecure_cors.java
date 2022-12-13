
public class Test {

	private static final String ALL_ORIGINS = "*";

	public WebFilter insecure1(){
		return (ServerWebExchange ctx, WebFilterChain chain)-> {
			ServerHttpRequest req = ctx.getRequest();

			if (CorsUtils.isCorsRequest(request)){
				ServerHttpResponse req = ctx.getResponse();
				HttpHeaders headers = response.getHeaders();
				headers.add("Access-Control-Allow-Origin", ALL_ORIGINS);  // Sensitive
			}
			return chain.filter(ctx);
		};
	}

  public void insecure2(CorsRegistry registry) {
    registry.addMapping("/**").allowedOrigins("*"); // Sensitive
  }

	public void insecure3() {
    CorsConfiguration config = new CorsConfiguration();
		config.addAllowedOrigin(ALL_ORIGINS); // Sensitive
  }

	public void secure() {
		String ALLOWED_ORIGIN = "www.mytrustedorigin.com";
    CorsConfiguration config = new CorsConfiguration();
		config.addAllowedOrigin(ALLOWED_ORIGIN); // Safe
  }

}
